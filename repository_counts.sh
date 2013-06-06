echo capitals
<repositories.json json -C name | grep '[A-Z]' | wc -l
echo underscores
<repositories.json json -C name | grep _ | wc -l
echo hyphens
<repositories.json json -C name | grep - | wc -l
echo total
<repositories.json wc -l