###
#w2v.pl
#Scope: Defines the perl module to pull embeddings from a trained embedding model.
#Authors: Jeffrey Smith, Bill Cramer, Evan French
###

use strict;
use warnings;
use Word2vec::Interface;
use IO::Handle;

select(STDOUT); 
$| = 1;

my $source = $ARGV[0];
my $interface = Word2vec::Interface->new();
my $result = $interface->W2VReadTrainedVectorDataFromFile( "./" . $source );

if ($result != 0) {
    print "FAILED\n";
    exit;
}
else {
    print "READY\n";
}

while (1) {
    my $word = readline(STDIN);
    if(!defined($word)) {
        next;
    }
    chomp($word);
    if ($word eq "EXIT") {
        print("TRYING TO EXIT.");
        last;
    }
    my $result = $interface->W2VGetWordVector($word);
    if (defined($result)) {
        print($result);
        print("\n");
    }
    else {
        print("UNDEF\n");
    }
}

print "EXITED\n";

$interface->W2VClearVocabularyHash();

undef( $interface );