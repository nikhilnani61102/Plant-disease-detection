import cv2
import numpy as np
import glob

# x = input()
# original = cv2.imread(x+".jpg")
original = cv2.imread("apple_original.jpg")


sift = cv2.xfeatures2d.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(original, None)

index_params = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)



all_images_to_compare = []
titles = []
folders = []

for i in glob.iglob("images-comparison/*"):
    v = i.lstrip("images-comparison")
    v = v.strip("\\")
    folders.append(v)
print(folders)
count = 0
for i in folders:
    for f in glob.iglob("images-comparison/"+i+"/*"):
        image = cv2.imread(f)
        titles.append(f)
        all_images_to_compare.append(image)

    l = dict({0:"a"})
    for image_to_compare, title in zip(all_images_to_compare, titles):
        if original.shape == image_to_compare.shape:
            print("The images have same size and channels")
            difference = cv2.subtract(original, image_to_compare)
            b, g, r = cv2.split(difference)
            count +=1

            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                print("Similarity: 100% (equal size and channels)")
                break


        kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

        matches = flann.knnMatch(desc_1, desc_2, k=2)

        good_points = []
        for m, n in matches:
            if m.distance > 0.6*n.distance:
                good_points.append(m)

        number_keypoints = 0
        if len(kp_1) >= len(kp_2):
            number_keypoints = len(kp_1)
        else:
            number_keypoints = len(kp_2)

        print("Title: " + title)
        percentage_similarity = len(good_points) / number_keypoints * 100
        print("Similarity: " + str(int(percentage_similarity)) + "\n")
        if(percentage_similarity > list(l.keys())[0]):
            l.pop(list(l.keys())[0])
            l.update({int(percentage_similarity):title})
        # print(l.values())
# if count == 0:
#     print(l.values())
for i in l:
    aa = l[i]
print(aa)
if("tomato" in aa):
    print("Tomato defect found")
elif("potato" in aa):
    print("Potato defect found")
elif("apple" in aa):
    print("Apple defect found")

