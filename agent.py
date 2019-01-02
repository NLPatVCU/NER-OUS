"""
agent.py
Scope: Defines the Tensorflow Neural Network code used by the module.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
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
        prediction_dense = tf.layers.dense(inputs=l1_flat, units=self.num_classes, activation=None, use_bias=True, bias_initializer=self.initializer_bias, kernel_initializer=self.initializer, trainable=True)
        self.prediction = tf.reshape(prediction_dense, [-1, self.max_sentence_length, self.num_classes])

        #CRF Layer and Log Likelihood Error
        log_likelihood, transition_params = tf.contrib.crf.crf_log_likelihood(self.prediction, self.truth, self.seq_len)

        #Loss and Optimizer
        self.loss = tf.reduce_mean(-log_likelihood)

        self.update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(self.update_ops):
            self.optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(self.loss)

    def train(self, batch_x, batch_y, seq_len):
        """
        Function to train the network.

        :param batch_x: The data to be fed into the network.
        :param batch_y: The labels that the batch will be trained against.
        :param seq_len: The true length of each sentence in the batch.
        :return: loss as float.
        """
        loss, _ = self.sess.run([self.loss, self.optimizer], {self.input: batch_x, self.truth: batch_y, self.seq_len: seq_len})
        return loss

    def eval(self, batch_x, batch_y, seq_len):
        """
        Function to evaluate the network.

        :param batch_x: The data to be fed into the network.
        :param batch_y: The labels that the batch will be tested against.
        :param seq_len: The true length of each sentence in the batch.
        :return: Numpy array representing confusion matrix.
        """
        pred = self.sess.run(self.prediction, {self.input: batch_x, self.seq_len: seq_len})

        cfm = np.zeros((self.num_classes, self.num_classes), dtype=np.int32)

        for i in range(0, len(pred)):
            predi = pred[i, 0:seq_len[i], :]
            predi_argmax = np.argmax(predi, -1)

            for j in range(0, seq_len[i]):
                truth_class = int(batch_y[i][j])
                pred_class = int(predi_argmax[j])
                cfm[pred_class, truth_class] += 1

        return cfm

    def eval_with_structure(self, batch_x, batch_y, seq_len, k, file_map, batch_map, sentence_dict):
        """
        Function to evaluate the network in regards to original sentence structure.

        :param batch_x: The data to be fed into the network.
        :param batch_y: The labels that the batch will be tested against.
        :param seq_len: The true length of each sentence in the batch.
        :param k: The current bucket index.
        :param file_map: Map linking indices to files and sentences.
        :param batch_map: Map linking batches to indices for file_map.
        :param sentence_dict: Dictionary of our sentence structures.
        :return: Numpy array representing confusion matrix.
        """
        #TODO(Jeff) Remove batch_y from function.
        pred = self.sess.run(self.prediction, {self.input: batch_x, self.seq_len: seq_len})

        #Matrix in the form class,true span, partial span, wrong
        cfm = np.zeros((self.num_classes, 3), dtype=np.int32)

        #TODO(Jeff) Remove Debug features or implement properly.
        ##DEBUG FILE OUT##
        debug_file = open("debug.txt", "a")

        #For each index in k
        for i in range(0, len(pred)):
            predi = pred[i, 0:seq_len[i], :]
            predi_argmax = np.argmax(predi, -1)

            #Get the original file_map index.
            batch_index = batch_map[k][i]
            original_index = file_map[batch_index]
            y = sentence_dict[original_index[0]][original_index[1]]
            y_ = []

            #TODO(Jeff) Change this to use dynamic classes.
            #Build the tags in the sentence
            for j in range(0, seq_len[i]):
                pred_class = int(predi_argmax[j])
                if pred_class == 0:
                    y_.append(None)
                elif pred_class == 1:
                    y_.append("problem")
                elif pred_class == 2:
                    y_.append("test")
                elif pred_class == 3:
                    y_.append("treatment")

            #Add "END" for safe tagging.
            y_.append(None)

            #Append start/end tags
            j = 0
            #for j in range(0, len(y_)):
            while j < len(y_):
                if y_[j]:
                #if not y_[j] == None and not y_[j] == "":
                    cls = y_[j]

                    y_[j] = y_[j] + ":Start"
                    j += 1
                    while j < len(y_):
                        if not y_[j] == cls:
                            if not y_[j]:
                            #if y_[j] == "" or y_[j] == None:
                                y_[j] = cls + ":End"
                            else:
                                j -= 1
                            break

                        j += 1
                j += 1

            ##DEBUG STRINGS##
            out_text = "Text: "
            out_tags_truth = "Truth: "
            out_tags_pred = "Pred: "

            j_ = 0
            #for j_ in range(0, len(y_)):
            while j_ < (len(y_)-1):
                #if y.original_sentence_array[j_][1] == "" or y.original_sentence_array[j_][1] == None:
                if not y.original_sentence_array[j_][1]:
                    #if y_[j_] == "" or y_[j_] == None:
                    if not y_[j_]:
                        cfm[0, 0] += 1
                    else:
                        cfm[0, 2] += 1
                        debug_file.write("Text: " + str(y.original_sentence_array[j_][0]) +"\n") #DEBUG
                        debug_file.write("Truth: None\n") #DEBUG
                        debug_file.write("Pred: " + str(y_[j_]) + "\n\n") #DEBUG
                else:
                    cls = ""
                    if "problem" in y.original_sentence_array[j_][1]:
                        cls = 1
                    elif "test" in y.original_sentence_array[j_][1]:
                        cls = 2
                    elif "treatment" in y.original_sentence_array[j_][1]:
                        cls = 3
                    else:
                        cls = 0

                    if "Start" in y.original_sentence_array[j_][1]:
                        #Check for same start
                        write_flag = False #DEBUG
                        if y_[j_] == y.original_sentence_array[j_][1]:
                            #We have at least a partial start.
                            full_span = True

                            #Check the rest
                            while not "End" in y.original_sentence_array[j_][1] and j_ < len(y_)-1:
                                out_text = out_text + y.original_sentence_array[j_][0] + " " #Debug
                                out_tags_truth = out_tags_truth + str(y.original_sentence_array[j_][1]) + " " #Debug
                                out_tags_pred = out_tags_pred + str(y_[j_]) + " " #Debug
                                if not y_[j_] == y.original_sentence_array[j_][1]:
                                    full_span = False
                                j_ += 1

                            if full_span:
                                cfm[cls, 0] += 1
                            else:
                                cfm[cls, 1] += 1
                                write_flag = True

                        else:
                            cfm[cls, 2] += 1
                            write_flag = True
                            while not "End" in y.original_sentence_array[j_][1] and j_ < len(y_)-1:
                                out_text = out_text + y.original_sentence_array[j_][0] + " " #Debug
                                out_tags_truth = out_tags_truth + str(y.original_sentence_array[j_][1]) + " " #Debug
                                out_tags_pred = out_tags_pred + str(y_[j_]) + " " #Debug
                                j_ += 1

                        if write_flag:
                            out_text = out_text + y.original_sentence_array[j_][0] + " " #Debug
                            out_tags_truth = out_tags_truth + str(y.original_sentence_array[j_][1]) + " " #Debug
                            out_tags_pred = out_tags_pred + str(y_[j_]) + " " #Debug
                            debug_file.write(out_text + "\n")
                            debug_file.write(out_tags_truth + "\n")
                            debug_file.write(out_tags_pred + "\n\n")
                            out_text = "Text: "
                            out_tags_truth = "Truth: "
                            out_tags_pred = "Pred: "

                    else:
                        if y_[j_] == y.original_sentence_array[j_][1]:
                            cfm[cls, 0] += 1
                        else:
                            cfm[cls, 2] += 1
                            debug_file.write("Text: " + str(y.original_sentence_array[j_][0]) +"\n") #DEBUG
                            debug_file.write("Truth: " + str(y.original_sentence_array[j_][1]) +"\n") #DEBUG
                            debug_file.write("Pred: " + str(y_[j_]) + "\n\n") #DEBUG

                j_ += 1

        debug_file.close()
        return cfm

    def clean_up(self):
        """
        Function to free resources of the network and reset the default graph.

        :return: Nothing.
        """
        self.sess.close()
        tf.reset_default_graph()
