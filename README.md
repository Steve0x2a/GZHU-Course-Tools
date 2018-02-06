# GZHU-Select_Course-Tools
[![versib](https://img.shields.io/badge/verson-0.1.1-lightgrey.svg)]()
[![Travis](https://img.shields.io/travis/rust-lang/rust.svg?style=flat-square)]()
[![language](https://img.shields.io/badge/language-Python3-blue.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

广州大学教务系统通识选修课选课脚本

---
## Requirements 
Python 3 +Requests + BeautifulSoup4 + lmxl +fire

使用`pip install -r requirements.txt`安装本脚本所需要依赖

## Usage 
#### 基本用法 
运行`python run.py refresh '用户名' '密码'`
更新cookie以及课程表

在`data/course_list.json`中可以查看选课课表情况

运行`python run.py select 选课编号 队列数(可选)`进行选课

其中队列数默认为10
#### 例子
```bash
$python run.py refresh '17xxxxxxxx' '123456'#刷新课表以及用户cookie
$python run.py select 102 #选择 '中国园林'课程
```

#### 注意事项
- 请尽量在选课前半小时前(选课网站还没崩之前)刷新课表以及用户cookie 

- 并且保证在选课网址已经无法使用情况下**不要刷新cookie**
**不要刷新** **不要刷新** **不要刷新**  直接运行`python select 课程编号`即可
- 请**不要泄露**data/cookies中的文件 泄露可能导致教务网站信息被盗用

## 原理
见docs文件夹(待完成
## TO DO
- 完善cookie管理系统
- 实时监测是否选课成功