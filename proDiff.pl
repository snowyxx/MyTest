#!perl -w
use strict;
my $arglength = @ARGV;
if ( $arglength != 3 ) {
	&usage;
}
my $option         = shift @ARGV;
my $firstFileName  = shift @ARGV;
my $secondFileName = shift @ARGV;

my %firstFile;
my %secondFile;

if ( $option eq "-c" ) {
	%firstFile  = &fileToHash($firstFileName);
	%secondFile = &fileToHash($secondFileName);
	&copyValue( \%firstFile, \%secondFile );
}
elsif ( $option eq "-d" ) {
	%firstFile  = &fileToHash($firstFileName);
	%secondFile = &fileToHash($secondFileName);
	&printDiff( \%firstFile, \%secondFile );
}
elsif ( $option eq "-s" ) {
	%firstFile  = &fileToHash($firstFileName);
	%secondFile = &fileToHash($secondFileName);
	&printDiff_more( \%firstFile, \%secondFile );
}
elsif ( $option eq "-r" ) {
	print
"\n###################��һ���ļ� $firstFileName�ļ����ظ���key��\n";

	&checkDup($firstFileName);
	print
"\n###################�ڶ����ļ� $secondFileName�ļ����ظ���key��\n";

	&checkDup($secondFileName);
}
elsif ( $option eq "-D" ) {
	&delSameLine($firstFileName,$secondFileName)
}
else {
	&usage;
}

#����=�ŷָ����ļ�ÿ�зŵ�hash��
sub fileToHash {
	my $file = shift @_;
	my %fileHash;
	open( FILE, "$file" ) || die "���ļ�ʧ�ܣ�$!\n";
	while (<FILE>) {
		chomp;
		my $line=$_;
		unless ( ( $line =~ /^#/ ) || ( $line =~ /^\s+$/ ) ) {
			(index( $line, "=" ) > -1)?my $ind=index( $line, "=" ):next;
			my $keyname = substr( $line, 0, $ind );
			my $keyvalue = substr( $line, $ind + 1 );
			$keyname=&trim($keyname);
			$keyvalue=&trim($keyvalue);
			$fileHash{$keyname} = $keyvalue;
		}
	}

	close FILE;
	return %fileHash;
}

#�ѵڶ����ļ��е�ֵ���Ƹ���һ���ļ���������ͬ��key��ͬʱ�г�û�г����ڵڶ����ļ��е�key
sub copyValue {
	my $first  = shift @_;
	my $second = shift @_;
	my %result;

	foreach my $firstEntry ( keys %$first ) {
		foreach my $secondEntry ( keys %$second ) {
			if ( $firstEntry eq $secondEntry ) {
				$result{$firstEntry} = $$second{$secondEntry};
				delete $$first{$firstEntry};
			}
		}
	}
	foreach ( keys %result ) {
		print "$_", "=", "$result{$_}\n";
	}
	print
	  "\n###################----------ֻ�����ڵ�һ���ļ��е�key\n";
	foreach ( keys %firstFile ) {
		print "$_", "=", "$$first{$_}\n";
	}
}

#��ӡ������hash��key��ͬ�ĸ�������
sub printDiff {
	my $first  = shift @_;
	my $second = shift @_;

	foreach my $firstEntry ( keys %$first ) {
		foreach my $secondEntry ( keys %$second ) {
			if ( $firstEntry eq $secondEntry ) {

				#				delete $$first{$secondEntry};
				#				delete $$second{$secondEntry};
				delete( $first->{$secondEntry} );
				delete( $second->{$secondEntry} );
			}
		}
	}
	print
"\n###################----------��һ���ļ����е�key------------\n";
	foreach ( keys %$first ) {
		print "$_", "=", "$$first{$_}\n";
	}
	print
"\n###################----------�ڶ����ļ����е�key------------\n";
	foreach ( keys %$second ) {
		print "$_", "=", "$$second{$_}\n";
	}
}

#��sub printDiff���˱Ƚ�key����ͬ��ʱ��keyֵ�Ƿ�Ҳ��ͬ
sub printDiff_more {
	my $first  = shift @_;
	my $second = shift @_;
print
"\n###################----------�����ļ���ֵ��ͬ��key------------\n";
	foreach my $firstEntry ( keys %$first ) {
		foreach my $secondEntry ( keys %$second ) {
			if ( $firstEntry eq $secondEntry ) {
				if(($first->{$secondEntry}) ne ($second->{$secondEntry})){
					print "< $firstEntry=$first->{$secondEntry}\n";
					print "> $secondEntry=$second->{$secondEntry}\n\n";
				}
				delete( $first->{$secondEntry} );
				delete( $second->{$secondEntry} );
			}
		}
	}
	print
"\n###################----------��һ���ļ����е�key------------\n";
	foreach ( keys %$first ) {
		print "$_", "=", "$$first{$_}\n";
	}
	print
"\n###################----------�ڶ����ļ����е�key------------\n";
	foreach ( keys %$second ) {
		print "$_", "=", "$$second{$_}\n";
	}
}

#�����һ���ļ��з����ظ���key
sub checkDup {
	my $file = shift @_;
	open FF, "$file";
	my @allkeys;
	my %count;

	while (<FF>) {
		chomp;
		if ( ( $_ =~ /^#/ ) || ( $_ =~ /^\s+$/ ) ) { }
		else {
			my $line = $_;
			my $ind = index( $line, "=" );
			my $keyname = substr( $line, 0, $ind );
			$keyname=&trim($keyname);
			push @allkeys, $keyname;
		}
	}

	foreach (@allkeys) {
		$count{$_}++;
	}
	foreach ( keys %count ) {
		if ( $count{$_} > 1 ) {
			print "$_\n";
		}
	}

	close FF;

}

#�ڵ�һ���ļ���ɾ�������ڵڶ����ļ����У�������ɾ������properteis�ж��key)
sub delSameLine{
	#print "I ma here....\n";
	my $f1=shift @_;
	my $f2=shift @_;
	open( FILE1, "$f1" ) || die "���ļ�ʧ�ܣ�$!\n";
	open( FILE2, "$f2" ) || die "���ļ�ʧ�ܣ�$!\n";
	my @f1=<FILE1>;
	my @f2=<FILE2>;
	
	my %h;
	my %a;
	map{chomp;$_=&trim($_);$a{$_}++;$h{$_}++}@f1; 
	map{chomp;$_=&trim($_);$h{$_}++}@f2;
	foreach (keys %h){
		if ($h{$_}==1){
			print "$_\n" if exists $a{$_};
		}
	} 
	
	
}
sub trim
{
	my ($get_string) = @_;
	chomp($get_string);
	$get_string =~ s/^[\s]*//;
	$get_string =~ s/[\s]*$//;
	return $get_string;
}

sub usage {
	print "�������������ο������ʹ�÷�����\n";
	print(
		"Usage : proDiff.pl -<option> <filename1> <filename2>\n 
			-c: �ѵڶ����ļ��е�ֵ���Ƹ���һ���ļ���������ͬ��key��ͬʱ�г�û�г����ڵڶ����ļ��е�key\n
			-d: �Ƚϲ�ͬ���Ե��ļ����Ա������ļ��е�key�����г����Զ��е�key\n
			-s: �Ƚ���ͬ���Ե��ļ����Ա������ļ����г����Զ��е�key���Լ�ֵ��ͬ��key��\n
			-r: ��ʾ�����ļ��и����ظ���key������\n
			-D:	�ڵ�һ���ļ���ɾ�������ڵڶ����ļ����У�������ɾ������properteis�ж��key)"
	);
	exit 1;
}
