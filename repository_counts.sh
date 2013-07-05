echo capitals
cat repositories*.json json -C name | grep '[A-Z]' | wc -l
echo underscores
cat repositories*.json json -C name | grep _ | wc -l
echo hyphens
cat repositories*.json json -C name | grep - | wc -l
echo total
cat repositories*.json wc -l
