for max_hsv in $(seq 1 360); do 
    echo "Testing MAX_HSV=$max_hsv"
    python3 decipher.py 27 0 $max_hsv
done
