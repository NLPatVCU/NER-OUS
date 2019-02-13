"""
agent.py
Scope: Defines the Tensorflow Neural Network code used by the module.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
from copy import copy 

import tensorflow as tf
import numpy as np

#Author: Jeffrey Smith
class Agent:
    """
    Agent represents the neural network interface for Tensorflow that will train our data.
    """

    def __init__(self, num_features, num_classes, max_sentence_length, hidden_layer_size=256):
        """
        Constructor for Agent. Sets self parameters, builds the network, and initializes Tensorflow.
        :param num_features: The amount of features that will be present in the data.
        :param num_classes: The number of classes that will be present in the final results.
        :param max_sentence_length: The maximum number of characters that will be present in a sentence. If you go over, the network will throw an exception.
        :param hidden_layer_size: Number of nodes to have in the hidden layers. Defaults to 256.
        :return: Nothing.
        :var layer_size: Size of the hidden layers.
        :var max_sentence_length: The max length of a sentence.
        :var num_features: The numbers of features to be represented as input.
        :var num_classes: The number of classes in the final classification prediction.
        """
        self.layer_size = hidden_layer_size
        self.max_sentence_length = max_sentence_length
        self.num_features = num_features
        self.num_classes = num_classes

        self.build_network()

        self.sess = tf.Session()
        self.sess.run(tf.initializers.global_variables())

    def build_network(self):
        """
        Internal function to build the network of the agent.
        :return: Nothing.
        """
        #Initializers
        self.initializer = tf.contrib.layers.variance_scaling_initializer(dtype=tf.float32)
        self.initializer_bias = tf.zeros_initializer()

        #Inputs into the network.
        self.input = tf.placeholder(tf.float32, [None, self.max_sentence_length, self.num_features], name="input")
        self.truth = tf.placeholder(tf.int32, [None, self.max_sentence_length], name="truth") #A vector in the form [BatchSize,SentenceLength]
        self.seq_len = tf.placeholder(tf.int32, [None], name="seq_len")

        #LSTM Cells and RNN
        lstm_fw_cell = tf.nn.rnn_cell.LSTMCell(self.layer_size, forget_bias=1.0, name="forward_cell", dtype=tf.float32)
        lstm_rv_cell = tf.nn.rnn_cell.LSTMCell(self.layer_size, forget_bias=1.0, name="reverse_cell", dtype=tf.float32)

        (fw_out, bw_out), l1_output_states = tf.nn.bidirectional_dynamic_rnn(lstm_fw_cell, lstm_rv_cell, inputs=self.input, sequence_length=self.seq_len, dtype=tf.float32)

        #Reshape data for Dense layer.
        l1_concat = tf.concat([fw_out, bw_out], axis=-1)
        l1_flat = tf.reshape(l1_concat, [-1, 2*self.layer_size])

        #Dense Layer and Reshape
        self.dropperc = tf.placeholder(tf.float32)
        l1_drop = tf.nn.dropout(l1_flat, self.dropperc)
        prediction_dense = tf.layers.dense(inputs=l1_drop, units=self.num_classes, activation=None, use_bias=True, bias_initializer=self.initializer_bias, kernel_initializer=self.initializer, trainable=True)
        self.prediction = tf.reshape(prediction_dense, [-1, self.max_sentence_length, self.num_classes])

        #CRF Layer and Log Likelihood Error
        log_likelihood, transition_params = tf.contrib.crf.crf_log_likelihood(self.prediction, self.truth, self.seq_len)

        #Loss and Optimizer
        self.loss = tf.reduce_mean(-log_likelihood)

        self.update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(self.update_ops):
            self.optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(self.loss)
            
        #Model Saver
        self.saver = tf.train.Saver()

    def save_model(self, file_path):
        self.saver.save(self.sess, file_path)
        
    def load_model(self, file_path):
        self.saver.restore(self.sess, file_path)

    def train(self, batch_x, batch_y, seq_len):
        """
        Function to train the network.
        :param batch_x: The data to be fed into the network.
        :param batch_y: The labels that the batch will be trained against.
        :param seq_len: The true length of each sentence in the batch.
        :return: loss as float.
        """
        loss, _ = self.sess.run([self.loss, self.optimizer], {self.input: batch_x, self.truth: batch_y, self.seq_len: seq_len, self.dropperc: 0.5})
        return loss

    def eval_token_level(self, batch_x, batch_y, seq_len):
        """
        Function to evaluate network at the token level for a ground truth set.
        :param batch_x: The data to be fed into the network.
        :param batch_y: The labels that the batch will be tested against.
        :param seq_len: The true length of each sentence in the batch.
        :return: (NxN) confusion matrix representing confusion matrix.
        """
        pred = self.sess.run(self.prediction, {self.input: batch_x, self.seq_len: seq_len, self.dropperc: 1.0})

        confusion_matrix = np.zeros((self.num_classes, self.num_classes), dtype=np.int32)

        for i in range(0, len(pred)):
            predi = pred[i, 0:seq_len[i], :]
            predi_argmax = np.argmax(predi, -1)

            for j in range(0, seq_len[i]):
                truth_class = int(batch_y[i][j])
                pred_class = int(predi_argmax[j])
                confusion_matrix[pred_class, truth_class] += 1

        return confusion_matrix

    def eval_phrase_level(self, batch_x, seq_len, k, file_map, batch_map, sentence_dict, config):
        """
        Function to evaluate the network at the phrase level for a ground truth set.
        :param batch_x: The data to be fed into the network.
        :param seq_len: The true length of each sentence in the batch.
        :param k: The current bucket index.
        :param file_map: Map linking indices to files and sentences.
        :param batch_map: Map linking batches to indices for file_map.
        :param sentence_dict: Dictionary of our sentence structures.
        :return: Numpy array representing confusion matrix.   (Nx4) matrix representing phrase level characteristics. COR/PAR/MIS/SUP
        """
        pred = self.sess.run(self.prediction, {self.input: batch_x, self.seq_len: seq_len, self.dropperc: 1.0})

        #Matrix in the form class,true span, partial span, wrong
        phrase_matrix = np.zeros((self.num_classes, 4), dtype=np.int32)

        #Debug
        if "DEBUG" in config['CONFIGURATION']:
            debug_file = open('debug.txt', 'a')
            
        #For each index in bucket k 
        for i in range(0, len(pred)):
            i_pred = pred[i, 0:seq_len[i], :]
            i_pred_argmax = np.argmax(i_pred, -1)
   
            #Get the original file_map index.
            batch_index = batch_map[k][i]
            original_index = file_map[batch_index]
            y = sentence_dict[original_index[0]][original_index[1]]
            

            #Build sentence tags
            y_ = build_sentence_tags(config, seq_len[i], i_pred_argmax)
                
            #Add Tags to Modified Sentence
            for m, el in enumerate(y.modified_sentence_array):
                el[1] = y_[m]
                
            #Rebuild Modified Sentence
            y.rebuild_modified_sentence_array()
                
            #Find each phrase group in original sentence and check it against predicted values.
            truth_start, truth_end, truth_class = get_annotation(y.original_sentence_array, 0)
            pred_start, pred_end, pred_class = get_annotation(y.modified_sentence_array, 0)
            
            while True:
                if not truth_start == None and not pred_start == None:
                    if is_overlapped(truth_start, truth_end, pred_start, pred_end) == 0:
                        if truth_class == pred_class and truth_start == pred_start and truth_end == pred_end:
                            #CORRECT
                            phrase_matrix[config['CLASS_MAP'][truth_class]][0] += 1
                            
                            
                            #Debug
                            if "DEBUG" in config['CONFIGURATION']:
                                start_ = min(truth_start, pred_start)
                                end_ = max(truth_end, pred_end)
                                
                                write_phrase_debug_line(debug_file, start_, end_, y, "COR", truth_start, truth_end, pred_start, pred_end)
                            
                            
                            truth_start, truth_end, truth_class = get_annotation(y.original_sentence_array, truth_end+1)
                            pred_start, pred_end, pred_class = get_annotation(y.modified_sentence_array, pred_end+1)

                        else:
                            #PARTIAL
                            phrase_matrix[config['CLASS_MAP'][truth_class]][1] += 1
                            
                            #Debug
                            if "DEBUG" in config['CONFIGURATION']:
                                start_ = min(truth_start, pred_start)
                                end_ = max(truth_end, pred_end)
                                
                                write_phrase_debug_line(debug_file, start_, end_, y, "PAR", truth_start, truth_end, pred_start, pred_end)
                                
                            truth_start, truth_end, truth_class = get_annotation(y.original_sentence_array, truth_end+1)
                            pred_start, pred_end, pred_class = get_annotation(y.modified_sentence_array, pred_end+1) 
                    elif is_overlapped(truth_start, truth_end, pred_start, pred_end) == -1:
                        #Pred is to the left, mark SUP and iterate.
                        phrase_matrix[config['CLASS_MAP'][pred_class]][3] += 1
                        
                        #Debug
                        if "DEBUG" in config['CONFIGURATION']:
                            write_phrase_debug_line(debug_file, pred_start, pred_end, y, "SUPL_TP", truth_start, truth_end, pred_start, pred_end)
                            
                        pred_start, pred_end, pred_class = get_annotation(y.modified_sentence_array, pred_end+1)
                    else:
                        #Pred is to the right, mark MIS and iterate.
                        phrase_matrix[config['CLASS_MAP'][truth_class]][2] += 1
                        
                        #Debug
                        if "DEBUG" in config['CONFIGURATION']:
                            write_phrase_debug_line(debug_file, truth_start, truth_end, y, "MIS", truth_start, truth_end, pred_start, pred_end)
                            
                        truth_start, truth_end, truth_class = get_annotation(y.original_sentence_array, truth_end+1)
                elif truth_start:
                    #Missing Pred, mark MIS and iterate.
                    phrase_matrix[config['CLASS_MAP'][truth_class]][2] += 1
                    
                    #Debug
                    if "DEBUG" in config['CONFIGURATION']:
                        write_phrase_debug_line(debug_file, truth_start, truth_end, y, "MIS", truth_start, truth_end, pred_start, pred_end)

                    truth_start, truth_end, truth_class = get_annotation(y.original_sentence_array, truth_end+1)
                elif pred_start:
                    #Superficial Pred, mark SUP and iterate.
                    phrase_matrix[config['CLASS_MAP'][pred_class]][3] += 1
                    
                    #Debug
                    if "DEBUG" in config['CONFIGURATION']:
                        write_phrase_debug_line(debug_file, pred_start, pred_end, y, "SUP", truth_start, truth_end, pred_start, pred_end)
                        
                    pred_start, pred_end, pred_class = get_annotation(y.modified_sentence_array, pred_end+1)
                else:
                    #Nothing else.
                    break

        #Debug
        if "DEBUG" in config['CONFIGURATION']:
            debug_file.close()
            
        return phrase_matrix
        
    def build_annotations(self, batch_x, seq_len, file_map, batch_map, sentence_dict, k, config):
        pred = self.sess.run(self.prediction, {self.input: batch_x, self.seq_len: seq_len, self.dropperc: 1.0})

        #For each index in the prediction, rebuild sentence 
        for i in range(0, len(pred)):
            i_pred = pred[i, 0:seq_len[i], :]
            i_pred_argmax = np.argmax(i_pred, -1)
   
            #Get the original file_map index.
            batch_index = batch_map[k][i]
            original_index = file_map[batch_index]
            y = sentence_dict[original_index[0]][original_index[1]]

            #Build sentence tags
            y_ = build_sentence_tags(config, seq_len[i], i_pred_argmax)
                
            #Add Tags to Modified Sentence
            for m, el in enumerate(y.modified_sentence_array):
                el[1] = y_[m]
                
            #Rebuild Modified Sentence
            y.rebuild_modified_sentence_array()

    def clean_up(self):
        """
        Function to free resources of the network and reset the default graph.
        :return: Nothing.
        """
        self.sess.close()
        tf.reset_default_graph()
        
def get_annotation(sentence_array, start_index):
    if start_index >= len(sentence_array):
        return None, None, None

    start, end, tag = -1, -1, ''

    for j in range(start_index, len(sentence_array)):
        if start > -1:
            if sentence_array[j][1] == tag:
                continue
            else:
                end = j-1
                return start, end, tag
        else:
            if not sentence_array[j][1] == '':
                start = j
                tag = sentence_array[j][1]

    if start > -1:
        return start, len(sentence_array)-1, tag
    else:
        return None, None, None

def is_overlapped(x_start, x_end, y_start, y_end):
    if ((y_start >= x_start and y_end <= x_end) or (y_end >= x_start and y_start <= x_start) or (y_start <= x_end and y_end >= x_end)):
        return 0
    elif (y_end < x_start):
        return -1
    else:
        return 1
     
def build_sentence_tags(config, seq_len, pred_class_list):
    #Build sentence tags
    return_class_list = []
    for j in range(0, seq_len):
        pred_class = int(pred_class_list[j])
        if pred_class > 0:
            return_class_list.append(config['CLASS_LIST'][pred_class-1].lower())
        else:
            return_class_list.append('')     
    return return_class_list
            
def write_phrase_debug_line(debug_file, start, end, ss, type, x1, x2, y1, y2):
    debug_file.write(type + "\n")
    out_text_ = "Text: "
    out_truth_ = "Truth: "
    out_pred_ = "Pred: "  
    
    #for o in range(start, end+1):
    for o in range(0, len(ss.original_sentence_array)):
        out_text_ += ss.original_sentence_array[o][0] + " "
        if not ss.original_sentence_array[o][1] == '':
            out_truth_ += ss.original_sentence_array[o][1][0:4] + " "
        else:
            out_truth_ += 'none' + ' '
        if not ss.modified_sentence_array[o][1] == '':
            out_pred_ += ss.modified_sentence_array[o][1][0:4] + " "
        else:
            out_pred_ += 'none' + ' '
    debug_file.write(out_text_ + "\n")
    debug_file.write(out_truth_ + "\n")
    debug_file.write(out_pred_ + "\n")
    if not x1 == None and not ss.original_sentence_array[x1][1] == '':
        debug_file.write("Tag: " + str(ss.original_sentence_array[x1][1]) + '\n')
    else:
        debug_file.write("Tag: none\n")
    debug_file.write('Ranges: ' + str(x1) + ',' + str(x2) + ';' + str(y1) + ',' + str(y2) + '\n\n')
