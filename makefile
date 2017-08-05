test:
	gnome-terminal  \
	--window  \
	--tab -e 'bash -c "perl  gupc.pl 600000;exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 601000 ; exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 602000 ; exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 603000 ; exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 604000 ; exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 605000 ; exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 606000 ; exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 607000 ; exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 608000 ; exec bash"' \
	--tab -e 'bash -c "perl  gupc.pl 609000 ; exec bash"' 
run:
#	perl gupc.pl
	head -n 20 sum.csv > sum_20.csv
	perl send_mail.pl
file_date = $(shell date +%y_%m_%d_%02k_%M)
test1:
	echo $(file_date);
r:
	cd gupc_data;rm -rf *;
	perl gupc.pl 0 220;
	perl gupc.pl 300000 70;
	perl gupc.pl 600000 380;
	perl gupc.pl csv;
	cp sum.csv sum_$(file_date).csv;
	perl send_mail.pl sum_$(file_date).csv;
	rm sum_$(file_date).csv;
	shutdown;

g:
	cd gupc_data;rm -rf *;
	python ../../python_sp/gupc/gupc.py 0 220 ;
	python ../../python_sp/gupc/gupc.py 300000 70;
	python ../../python_sp/gupc/gupc.py 600000 380;
	perl gupc.pl csv;
	cp sum.csv sum_$(file_date).csv;
	perl send_mail.pl sum_$(file_date).csv;
	rm sum_$(file_date).csv;
	shutdown;

