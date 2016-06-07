# echo "mail"
Directory=/var/www/html/OCR++/myproject/media/documents

python $Directory/printMailformap.py <<EOF
$f
EOF

# echo "name"
python $Directory/printnameformap.py
# echo "map"
python $Directory/email_matching.py > $Directory/map.txt