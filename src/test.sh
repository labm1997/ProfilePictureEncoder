echo "== Rectangular profile test =="
echo "Encoding:"
echo "abcdefghijklmnopqrstuvwxyz ,:.?-"
python3 rectangular_encode.py "abcdefghijklmnopqrstuvwxyz ,:.?-" test_rectangular.png
echo "Decoding"
python3 rectangular_decode.py test_rectangular.png 6

echo "== Circular profile test ==
"echo "Encoding:"
echo "abcdefghijklmnopqrstuvwxyz ,:.?-"
python3 circular_encode.py "abcdefghijklmnopqrstuvwxyz ,:.?-" test_circular.png --scale 4.5

echo "Decoding"
python3 circular_decode.py test_circular.png

echo "== Circular profile test ==
"echo "Encoding:"
echo "voce, que tem ideias tao modernas. e o mesmo homem que vivia nas cavernas."
python3 circular_encode.py "voce, que tem ideias tao modernas. e o mesmo homem que vivia nas cavernas." test_profile.png --scale 3.4

echo "Decoding"
python3 circular_decode.py test_profile.png