#!/usr/bin/perl
use strict;
use warnings;

sub print_welcome {
    print "**********************************\n";
    print "Welcome to ChatBot!\n";
    print "* Type Hello to begin *\n";
    print "**********************************\n\n";
}

sub input_prompt {
    print "------------------------------------\n";
    print "User Input: ";
    my $input = <>;
    chomp($input);
    return $input;
}

sub process_regex_substitution{
    my $regex_substitution = $_[0];

    $regex_substitution =~ s/^(Hh]ello|[Hh]i)$/Hello user! What is your name?\n/g;
    $regex_substitution =~ s/^[Mm]y name is (\w+)$/Hello \1! How can I assist you today?\n/g;

    $regex_substitution =~ s/^((\w+\s)+)(has|is) (stopped working completely|partially working)$/Since \1 \3 \4, have you tried turning it off and on again?\n/g;
    $regex_substitution =~ s/^Yes, I have tried (.+) and it is still (broken|not working|malfunctioning|faulty)$/If \1 did not resolve the issue and the product is still \2, then kindly contact our customer care line at 0800 123 4567\n/g;
    $regex_substitution =~ s/^Yes, I have (.+) and the product is (working|functioning|operational) again$/That is great news that you \1 has put the product back into a \2 state! Is there anything else that I can assist with?/g;
    $regex_substitution =~ s/^No, there is nothing else$/Ok great, have a pleasant day further. Goodbye/g;

    # Change 'my' to 'our'
    $regex_substitution =~ s/[Mm]y/our/g;
    $regex_substitution =~ s/^I am having (trouble|issues|difficulties|complications) with ((\w|\s)+)$/I am sorry to hear that you are experiencing \1 with \2 product! Is \2 partially working or has it stopped working completely?\n/g;

    if ($regex_substitution =~ $_[0]){
        print "ChatBot output: I am sorry, I did not understand your input. Please try again.\n";
    }else {
        print "ChatBot output: ", $regex_substitution, "\n";
    }
    return $regex_substitution
}

my $output = "";
&print_welcome();
while($output !~ m/Goodbye/){
    my $user_input = &input_prompt();
    $output = &process_regex_substitution($user_input);
}
print "\n\n"
