#include<iostream>
#include<vector>
#include<string>
#include<algorithm>
#include<math.h>
using namespace std;
//lower case
string binToHex(string a)
{
	string val;
	int decimalVal;
	for(int i=0;i<a.size();i++)
		decimalVal+=(a[i]-'0')*pow(2,a.size()-1-i);
	if(decimalVal>9)
	{
		val=char(decimalVal-10+97);
	}
	else
		val=decimalVal+'0';
	return val;
}
//binary to decimal func
int binToDec(string a)
{
	int val=0;
	int counter=0;
	for(int i=a.size()-1;i>=0;i--)
	{
		val+=(a[i]-'0')*pow(2,counter);
		counter++;
	}
	return val;
}
string toBin(int a)
{
	string val;
	while(a!=0)
	{
		val.push_back((a%2)+'0');
		a=a/2;
	}
	reverse(val.begin(),val.end());
	for(int i=val.size();i<4;i++)
	{
		val.insert(0,1,'0');
	}
	return val;
}

string toHex(string input)
{
	string returnVal;
	for(int i=0;i<input.size();i++)
	{
		//abcdef
		if(int(input[i])>=97)
		{
			string val=toBin(int(input[i])-97+10);
			returnVal+=val;
		}
		else if(int(input[i])>=65 && int(input[i])<97)
		{
			string val=toBin(int(input[i])-65+10);
			returnVal+=val;
		}
		else
		{
			string val=toBin(input[i]-'0');
			returnVal+=val;
		}
	}
	return returnVal;
}
string expanFunc(string input)
{
int eTable[]={
32,	1,	2,	3,	4,	5,
4,	5,	6,	7,	8,	9,
8,	9,	10,	11,	12,	13,
12,	13,	14,	15,	16,	17,
16,	17,	18,	19,	20,	21,
20,	21,	22,	23,	24,	25,
24,	25,	26,	27,	28,	29,
28,	29,	30,	31,	32,	1,
};
string val;
for(int i=0;i<48;i++)
{
	val+=input[eTable[i]-1];
}
return val;
}
string xorFunc(string a, string b)
{
	string val;
	for(int i=0;i<a.size();i++)
	{
		if(a[i]==b[i])
			val.push_back('0');
		else
			val.push_back('1');
	}
	return val;
}
string sBoxFunc(string a)
{
	string returnVal;
	//sBox1
	int sBox1[4][16]={  
		{14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7},  
		{0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8},  
		{4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0}, 
		{15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13} 
	};
	string rowStr, colStr;
	int row, col;
	for(int i=0;i<6;i++)
	{
		if(i%6==0||i%6==5)
			rowStr+=a[i];
		else
			colStr+=a[i];
	}
	row=binToDec(rowStr);
	col=binToDec(colStr);
	returnVal+=toBin(sBox1[row][col]);
	rowStr.clear();
	colStr.clear();
	//sbox2
	int sBox2[4][16]={
		{15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10},  
		{3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5}, 
		{0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15},  
		{13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9}
	};
	for(int i=6;i<12;i++)
	{
		if(i%6==0||i%6==5)
			rowStr+=a[i];
		else
			colStr+=a[i];
	}
	row=binToDec(rowStr);
	col=binToDec(colStr);
	returnVal+=toBin(sBox2[row][col]);
	rowStr.clear();
	colStr.clear();
	//sbox3
	int sBox3[4][16]={
		{10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8},  
		{13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1},  
		{13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7},  
		{1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12}
	};
	for(int i=12;i<18;i++)
	{
		if(i%6==0||i%6==5)
			rowStr+=a[i];
		else
			colStr+=a[i];
	}
	row=binToDec(rowStr);
	col=binToDec(colStr);
	returnVal+=toBin(sBox3[row][col]);
	rowStr.clear();
	colStr.clear();
	//sbox4
	int sBox4[4][16]={
		{7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15},  
		{13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9},  
		{10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4},  
		{3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14}
	};
	for(int i=18;i<24;i++)
	{
		if(i%6==0||i%6==5)
			rowStr+=a[i];
		else
			colStr+=a[i];
	}
	row=binToDec(rowStr);
	col=binToDec(colStr);
	returnVal+=toBin(sBox4[row][col]);
	rowStr.clear();
	colStr.clear();
	//sbox5
	int sBox5[4][16]={
		{2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9},  
		{14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6},  
		{4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14},  
		{11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3}
	};
	for(int i=24;i<30;i++)
	{
		if(i%6==0||i%6==5)
			rowStr+=a[i];
		else
			colStr+=a[i];
	}
	row=binToDec(rowStr);
	col=binToDec(colStr);
	returnVal+=toBin(sBox5[row][col]);
	rowStr.clear();
	colStr.clear();
	//sbox6
	int sBox6[4][16]={
		{12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11},  
		{10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8},  
		{9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6},  
		{4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13}
	};
	for(int i=30;i<36;i++)
	{
		if(i%6==0||i%6==5)
			rowStr+=a[i];
		else
			colStr+=a[i];
	}
	row=binToDec(rowStr);
	col=binToDec(colStr);
	returnVal+=toBin(sBox6[row][col]);
	rowStr.clear();
	colStr.clear();
	//sbox7
	int sBox7[4][16]={
		{4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1},  
		{13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6},  
		{1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2},  
		{6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12}
	};
	for(int i=36;i<42;i++)
	{
		if(i%6==0||i%6==5)
			rowStr+=a[i];
		else
			colStr+=a[i];
	}
	row=binToDec(rowStr);
	col=binToDec(colStr);
	returnVal+=toBin(sBox7[row][col]);
	rowStr.clear();
	colStr.clear();
	//sbox8
	int sBox8[4][16]={
		{13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7},  
		{1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2},  
		{7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8},  
		{2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11}
	};
	for(int i=42;i<48;i++)
	{
		if(i%6==0||i%6==5)
			rowStr+=a[i];
		else
			colStr+=a[i];
	}
	row=binToDec(rowStr);
	col=binToDec(colStr);
	returnVal+=toBin(sBox8[row][col]);
	rowStr.clear();
	colStr.clear();

	return returnVal;
}
int main(int argc, char* argv[])
{
string input=argv[2];
string key=argv[1];
string output;
//delete 0x
input.erase(0,2);
key.erase(0,2);
//key transfer to 56bits
string hexKey;
hexKey=toHex(key);
int keyPC[]={
57,   49,   41,   33,    25,    17,    9,
 1,   58,   50,   42,    34,    26,   18,
10,    2,   59,   51,    43,    35,   27,
19,   11,    3,   60,    52,    44,   36,
63,   55,   47,   39,    31,    23,   15,
 7,   62,   54,   46,    38,    30,   22,
14,    6,   61,   53,    45,    37,   29,
21,   13,    5,   28,    20,    12,    4,
};
string newKey;//56bits new key
for(int i=0;i<56;i++)
{
	newKey+=hexKey[keyPC[i]-1];
}
//16 keys
vector<string >leftKey;
vector<string >rightKey;
//initial
string tmp="";
for(int i=0;i<28;i++)	
	tmp+=newKey[i];
leftKey.push_back(tmp);
string ttmp="";
for(int i=28;i<56;i++)
	ttmp+=newKey[i];
rightKey.push_back(ttmp);
//16 turns
for(int i=1;i<=16;i++)
{
	//shift one bit only
	if(i==1||i==2||i==9||i==16)
	{
		string tmp=leftKey[i-1];
		char insert=leftKey[i-1][0];
		tmp.erase(0,1);
		tmp+=insert;
		leftKey.push_back(tmp);

		string ttmp=rightKey[i-1];
		char insertR=rightKey[i-1][0];
		ttmp.erase(0,1);
		ttmp+=insertR;
		rightKey.push_back(ttmp);
	}
	//shift two bits
	else
	{
		string tmp=leftKey[i-1];
		char insert1=leftKey[i-1][0];
		char insert2=leftKey[i-1][1];
		tmp.erase(0,2);
		tmp+=insert1;
		tmp+=insert2;
		leftKey.push_back(tmp);

		string ttmp=rightKey[i-1];
		char insertR1=rightKey[i-1][0];
		char insertR2=rightKey[i-1][1];
		ttmp.erase(0,2);
		ttmp+=insertR1;
		ttmp+=insertR2;
		rightKey.push_back(ttmp);
	}
}
//combine left and right
vector<string >combineKey;
for(int i=1;i<=16;i++)
{
	string tmp;
	tmp=leftKey[i]+rightKey[i];
	combineKey.push_back(tmp);
}
vector<string >finalKey;
int keyPC2[]={
14,    17,   11,    24,    1,    5,
 3,    28,   15,     6,   21,   10,
23,    19,   12,     4,   26,    8,
16,     7,   27,    20,   13,    2,
41,    52,   31,    37,   47,   55,
30,    40,   51,    45,   33,   48,
44,    49,   39,    56,   34,   53,
46,    42,   50,    36,   29,   32,
};
//trans key to final 48bits
for(int j=0;j<16;j++)
{
	string trans;
	for(int i=0;i<48;i++)
	{
		trans+=combineKey[j][keyPC2[i]-1];
	}
	finalKey.push_back(trans);
}
string hexInput;
hexInput=toHex(input);
//initial permutation
int initialP[]={
58,	50,	42,	34,	26,	18,	10,	2,
60,	52,	44,	36,	28,	20,	12,	4,
62,	54,	46,	38,	30,	22,	14,	6,
64,	56,	48,	40,	32,	24,	16,	8,
57,	49,	41,	33,	25,	17,	9,	1,
59,	51,	43,	35,	27,	19,	11,	3,
61,	53,	45,	37,	29,	21,	13,	5,
63,	55,	47,	39,	31,	23,	15,	7
};
string initialPOutput;
for(int i=0;i<64;i++)
{
	initialPOutput+=hexInput[initialP[i]-1];
}

string lTmp, rTmp;
for(int i=0;i<32;i++)
	lTmp+=initialPOutput[i];
for(int i=32;i<64;i++)
	rTmp+=initialPOutput[i];

//permutation
int permuTable[]={
16,	7,	20,	21,
29,	12,	28,	17,
1,	15,	23,	26,
5,	18,	31,	10,
2,	8,	24,	14,
32,	27,	3,	9,
19,	13,	30,	6,
22,	11,	4,	25,
};
//16 times tranformation
for(int j=15;j>=0;j--)
{
	string now=xorFunc(finalKey[j],expanFunc(rTmp));
	now=sBoxFunc(now);
	//fin => function transfer final
	string fin;
	for(int i=0;i<32;i++)
	{
		fin+=now[permuTable[i]-1];
	}
	string oldRTmp=rTmp;
	rTmp=xorFunc(lTmp,fin);
	lTmp=oldRTmp;
}

//final left and right needed to be switch again!
string finalTransfer=rTmp;
finalTransfer+=lTmp;

int IP_1[]={
40,	8,	48,	16,	56,	24,	64,	32,
39,	7,	47,	15,	55,	23,	63,	31,
38,	6,	46,	14,	54,	22,	62,	30,
37,	5,	45,	13,	53,	21,	61,	29,
36,	4,	44,	12,	52,	20,	60,	28,
35,	3,	43,	11,	51,	19,	59,	27,
34,	2,	42,	10,	50,	18,	58,	26,
33,	1,	41,	9,	49,	17,	57,	25,
};

for(int i=0;i<64;i++)
{
	output+=finalTransfer[IP_1[i]-1];
}
vector<string > substrOutput;
string hexOutput;
//4bit one group
for(int i=0;i<64;i=i+4)
{
	string tmp=output.substr(i, 4);
	substrOutput.push_back(tmp);
}
for(int i=0;i<substrOutput.size();i++)
	hexOutput+=binToHex(substrOutput[i]);
//add 0x
hexOutput.insert(0,"0x");
cout<<hexOutput<<endl;
}
