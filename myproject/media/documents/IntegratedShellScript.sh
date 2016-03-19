Directory=myproject/media/documents

source ~/virtual_env/v1/bin/activate

$Directory/files/pdftoxml.linux64.exe.1.2_7 -noImage -noImageInline $Directory/input.pdf
$Directory/files/pdftoxml.linux64.exe.1.2_7 -noImage -noImageInline -l 2 $Directory/input.pdf $Directory/input_2.xml
#samuel
# rm $Directory/input.pdf
# echo "111"
# rm -r $Directory/input.xml_data

# echo "222"
$Directory/Clear.sh

# echo "1/10 section starting"
python $Directory/files/Secmapping.py > $Directory/Secmap.xml
python $Directory/create_eval_sections.py
echo "1/10 section done"
#samuel



#Priyank
# echo "2/10 Email and Affil starting"
python $Directory/Aff_new.py
python $Directory/Email_new.py
python $Directory/printEmail.py
python $Directory/printAff.py
echo "2/10 Email and Affil done"
#Priyank

# barno
# echo "3/10 Title starting"
python $Directory/files/TitleAuthor_parse.py
# echo "2/10 titleauthor parse done"
python $Directory/files/extra.py
# echo "3/10 extra done"
crf_test -m $Directory/files/model_all_com.txt $Directory/test_file.txt > $Directory/final.txt
python $Directory/files/TitleAuthorFinalTouch.py
# echo "4/10 final touch done"

python $Directory/files/printTitle.py > $Directory/TitleAuthor.xml
crf_test -m $Directory/files/model_all_com.txt $Directory/test_aut.txt > $Directory/final_aut.txt
echo "3/10 Title done"
# barno

# echo "4/10 Author starting"

python $Directory/files/printAuthor.py
echo "</title_author>" >> $Directory/TitleAuthor.xml
echo "4/10 Author done"
# #Tulasi
# echo "8/10 cit starting"
# python $Directory/cit2ref.py
# echo "8/10 cit done"
# #Tulasi
# echo "5/10 Mapping starting"
$Directory/Mapping.sh
echo "5/10 Mapping done"
#ayush
# echo "6/10 URL starting"
python $Directory/url.py > $Directory/URLop.txt
echo "6/10 URL done"
# echo "7/10 Footnotes starting"
python $Directory/footnotes.py > $Directory/FOOTNOTEop.txt
echo "7/10 Footnotes starting"
# echo "8/10 Tabfig starting"
python $Directory/tables_figures.py > $Directory/TABFIGop.txt
echo "8/10 Tabfig done"
# ayush

# rm $Directory/input.xml

#$Directory/Clean.sh

$Directory/eval_op.sh
echo "9/10 Printing done"
echo "10/10 Done Done Done"
