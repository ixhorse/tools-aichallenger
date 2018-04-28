#define _CRT_SECURE_NO_WARNINGS

#if defined(__linux__)
#include <dirent.h>
#include <sys/stat.h>
#elif defined(_WIN32)
#include <io.h>
#endif

#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <cmath>
#include <thread>
#include <errno.h>
#include <time.h>

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include <opencv2/imgproc.hpp>

#define pi 3.1415926 

using namespace std;

vector<string> listdir(string path);
string pathjoin(string root, char* file); 
void radial_trainsform(string path);
void worker(vector<string> path_list);

int main()
{
	vector<string> list;
	vector<string>::iterator iter;
	string path = "./image";

	int core = 8;
	vector<thread> t;
	vector<thread>::iterator iter_tmp;
	list = listdir(path);
	int length = list.size();
	int temp = ceil(length / core);

	cout << list.size() << endl;
	cout << "Allocating ...\n";
	for (int i = 0; i < core; ++i)
	{
		cout << "Starting thread" << i << '\n';
		vector<string> work_list;
		int start = i * temp;
		int end = (i + 1)*temp < length ? (i + 1)*temp : length;
		if (start > end)
			continue;
		work_list.assign(list.begin() + start, list.begin() + end);
		t.push_back(thread(worker, work_list));
	}
	for (iter_tmp = t.begin(); iter_tmp != t.end(); ++iter_tmp)
		(*iter_tmp).join();
	cout << "end" << endl;

	return 0;
}

void worker(vector<string> path_list)
{
	vector<string>::iterator iter;
    clock_t start, end;
	for (iter = path_list.begin(); iter != path_list.end(); ++iter)
	{
		start = clock();
		radial_trainsform(*iter);
		end = clock();
		cout << (double)(end - start)/CLOCKS_PER_SEC << endl;
	}
}

#if defined(_WIN32)
vector<string> listdir(string path)
{
	intptr_t handle;
	_finddata_t findData;
	string p = path;
	vector<string> list;
	
	p.append("\\*");
	handle = _findfirst(p.c_str(), &findData);
	if (handle == -1)
	{
		cout << "Failed first.\n";
		return list;
	}

	do
	{
		if (strcmp(findData.name, ".") == 0 || strcmp(findData.name, "..") == 0)
			continue;

		if (findData.attrib & _A_SUBDIR)
		{
			vector<string> new_list = listdir(pathjoin(path, findData.name));
			list.insert(list.begin(), new_list.begin(), new_list.end());
		}
		else
			list.push_back(pathjoin(path, findData.name));
	} while (_findnext(handle, &findData) == 0);

	_findclose(handle);

	return list;
}

string pathjoin(string root, char* file)
{
	string path = root;
	path.append("\\");
	path.append(file);
	return path;
}
#elif defined(__linux__)
vector<string> listdir(string path)
{
	DIR * dir;
	struct dirent * ptr;
	struct stat statbuf;
	vector<string> list;

	extern int errno;
	if((dir = opendir(path.c_str())) == NULL)
	{
		cout << "Can't open dir." << path << strerror(errno) << endl;
		return list;
	}
	while ((ptr = readdir(dir)) != NULL)
	{
		string sub_path = pathjoin(path, ptr->d_name);
		lstat(sub_path.c_str(), &statbuf);
		if (S_IFDIR & statbuf.st_mode)
		{
			if (ptr->d_name[0] == '.')
				continue;
			vector<string> new_list = listdir(sub_path);
			list.insert(list.begin(), new_list.begin(), new_list.end());
		}
		else
			list.push_back(sub_path);
	}
	closedir(dir);
	return list;
}
string pathjoin(string root, char* file)
{
	string path = root;
	path.append("/");
	path.append(file);
	return path;
}
#endif

void radial_trainsform(string path)
{
	using namespace cv;
	Mat img = imread(path);
	Mat img_new;

	resize(img, img_new, Size(224, 224));

	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			Mat img_radial = Mat::zeros(Size(224, 224), CV_8UC3);
			int u = 44 * i; //(u, v) radial polor
			int v = 44 * j;
			for (int m = 0; m < 224; m++)
			{
				for (int r = 0; r < 224; r++) // transform image
				{
					double theta = 2 * pi * m / 224;
					int x = u + round(r * cos(theta));
					int y = v + round(r * sin(theta));
					if (x >= 0 && x < 224 && y >= 0 && y < 224)
					{
						uchar* povec = img_new.ptr<uchar>(x, y); //original image
						uchar* prvec = img_radial.ptr<uchar>(m, r); //radial image
						for (int c = 0; c < img.channels(); c++)
						{
							*prvec++ = *povec++;
						}
						/*img_radial.at<Vec3b>(m, r) = img_new.at<Vec3b>(x, y);*/
					}
				}
			}
			//save image
			string path_new;
			char tail[10];
			sprintf(tail, "_%d.jpg", i * 5 + j);
			path_new.assign(path, 0, path.length()-4).append(tail);
			imwrite(path_new, img_radial);
		}
	}
}
