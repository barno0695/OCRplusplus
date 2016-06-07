Directory=/var/www/html/OCR++/myproject/media/documents

source ~/virtual_env/v1/bin/activate

$Directory/files/pdftoxml.linux64.exe.1.2_7 -noImage -noImageInline $Directory/input.pdf
$Directory/files/pdftoxml.linux64.exe.1.2_7 -noImage -noImageInline -l 2 $Directory/input.pdf $Directory/input_2.xml
#samuel
# rm $Directory/input.pdf
# echo "111"
# rm -r $Directory/input.xml_data

# echo "222"
$Directory/Clear.sh

# echo "1/12 section starting"
python $Directory/files/Secmapping.py > $Directory/Secmap.xml
python $Directory/create_eval_sections.py
echo "1/12 section done"
#samuel



#Priyank
# echo "2/12 Email and Affil starting"
python $Directory/Aff_new.py
python $Directory/Email_new.py
python $Directory/printEmail.py
python $Directory/printAff.py
echo "2/12 Email and Affil done"
#Priyank

# barno
# echo "3/12 Title starting"
python $Directory/files/TitleAuthor_parse.py
# echo "2/12 titleauthor parse done"
python $Directory/files/extra.py
# echo "3/12 extra done"
crf_test -m $Directory/files/model_all_com.txt $Directory/test_file.txt > $Directory/final.txt
python $Directory/files/TitleAuthorFinalTouch.py
# echo "4/12 final touch done"

python $Directory/files/printTitle.py > $Directory/TitleAuthor.xml
crf_test -m $Directory/files/model_all_com.txt $Directory/test_aut.txt > $Directory/final_aut.txt
echo "3/12 Title done"
# barno

# echo "4/12 Author starting"

python $Directory/files/printAuthor.py
echo "</title_author>" >> $Directory/TitleAuthor.xml
echo "4/12 Author done"
# #Tulasi
# echo "8/12 cit starting"
# python $Directory/cit2ref.py
# echo "8/12 cit done"
# #Tulasi
# echo "5/12 Mapping starting"
$Directory/Mapping.sh
echo "5/12 Mapping done"
#ayush
# echo "6/12 URL starting"
python $Directory/url.py > $Directory/URLop.txt
echo "6/12 URL done"
# echo "7/12 Footnotes starting"
python $Directory/footnotes.py > $Directory/FOOTNOTEop.txt
echo "7/12 Footnotes done"
# echo "8/12 Tabfig starting"
python $Directory/tables_figures.py > $Directory/TABFIGop.txt
echo "8/12 Tabfig done"
# ayush

rm $Directory/testResults/xmls/input.xml
rm $Directory/testResults/input.txt
rm $Directory/test_files/input.txt
$Directory/ref_extract.sh
echo "9/12 Reference feature extraction done"
# rm $Directory/input.xml

python $Directory/cit_final.py
# rm $Directory/input_cit2ref.xml
# cp /var/www/html/OCR++/input_cit2ref.xml $Directory
echo "10/12 Cit2ref done"

#$Directory/Clean.sh

$Directory/eval_op.sh
echo "11/12 Printing done"
echo "12/12 Done Done Done"
