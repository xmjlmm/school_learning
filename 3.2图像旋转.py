import cv2

fibe = cv2. imread("C://Users//86159//Desktop//test.jpg")

height, width = fibe.shape[ : 2 ]

M = cv2.getRotationMatrix2D((width/2, height/2), 60, 0.6)
rotate_fibe = cv2.warpAffine(fibe, M, (width, height))
cv2.namedWindow('Origin',cv2.WINDOW_NORMAL)
cv2.namedWindow('Rotation',cv2.WINDOW_NORMAL)
cv2.imshow("Origin",fibe)
cv2.imshow("Rotation", rotate_fibe)
cv2.waitKey()
cv2.destroyAllWindows( )