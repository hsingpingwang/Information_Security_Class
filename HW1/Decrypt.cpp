#include<iostream>
#include<math.h>
#include<algorithm>
#include<string>
#include<vector>
using namespace std;
string toBin(int a)
{
	string val;
	while(a!=0)
	{
		val.push_back((a%2)+'0');
		a=a/2;
	}
	reverse(val.begin(),val.end());
	for(int i=val.size();i<5;i++)
	{
		val.insert(0,1,'0');
	}
	return val;
}
int xorFunc(string a, string b)
{
	string val;
	int returnVal=0;
	for(int i=0;i<a.size();i++)
	{
		if(a[i]==b[i])
			val.push_back('0');
		else
			val.push_back('1');
	}
	for(int i=0;i<val.size();i++)
	{
		returnVal+=(val[i]-'0')*pow(2,val.size()-1-i);
	}
	return returnVal;
}
vector<int> lookTable(char table[5][5],char a)
{
	vector<int >val;
	for(int i=0;i<5;i++)
	{
		for(int j=0;j<5;j++)
		{
			if(table[i][j]==a)
			{
				val.push_back(i);
				val.push_back(j);
				break;
			}
		}
	}
	return val;
}

int main(int argc, char* argv[])
{
string input=argv[3];
string key=argv[2];
string cipherWay=argv[1];
string output;
if(cipherWay=="caesar")
{
	int index=0;
	for(int i=0;i<key.size();i++)
		index+=(key[i]-'0')*pow(10,(key.size()-i)-1);
	for(int i=0;i<input.size();i++)
	{
		if(input[i]-65+97-index<97)
		{
			//for backward more than char 97
			output.push_back(input[i]-65+97-index-97+123);
		}
		else
			output.push_back(input[i]-65+97-index);
	}
}
else if(cipherWay=="rail_fence")
{
	int index=0;
	for(int i=0;i<key.size();i++)
		index+=(key[i]-'0')*pow(10,(key.size()-i)-1);
	//separate times
	int count=input.size()/index;
	if(input.size()%index==0)
	{
		for(int j=0;j<count;j++)
		{
			for(int i=0;i<input.size();i=i+count)
			{
				char tmp=(input[i+j])-65+97;
				output.push_back(tmp);
			}
		}
	}
	else
	{
		int mod=input.size()%index;
		for(int j=0;j<count;j++)
		{
			int point=1;
			//contain remainder parts count++ since larger
			for(int i=0;i<input.size();i=i+count+1)
			{
				char tmp=(input[i+j])-65+97;
				output.push_back(tmp);
				point++;
				if(point>mod)
				{
					break;
				}
			
			}
			for(int i=mod*(count+1);i<input.size();i=i+count)
			{
				char tmp=(input[i+j])-65+97;
				output.push_back(tmp);
			}
			
		}
		//remainder part
		count+=1;
		for(int i=1;i<=mod;i++)
		{
			char tmp=(input[count*i-1])-65+97;
			output.push_back(tmp);
		}
	}
}
else if(cipherWay=="row")
{
	//create the array table
	vector<vector<int > >table;
	//resize 2*2 table
	int rowNum=0;
	if(input.size()%key.size()==0)
	{
		rowNum=input.size()/key.size();
		table.resize(rowNum);
		for(int i=0;i<rowNum;i++)
			table[i].resize(key.size(),0);
	}
	else
	{
		rowNum=input.size()/key.size()+1;
		table.resize(rowNum);
		for(int i=0;i<rowNum;i++)
			table[i].resize(key.size(),0);
		for(int i=input.size()%key.size();i<key.size();i++)
		{
			table[rowNum-1][i]=-1;
		}
	}
	vector<int >indexArray;
	for(int i=1;i<=key.size();i++)
	{
		//get index
		for(int j=0;j<key.size();j++)
		{
			if(key[j]-'0'==i)
				indexArray.push_back(j);
		}
	}
	int inputPtr=0;
	for(int i=0;i<indexArray.size();i++)
	{
		for(int j=0;j<rowNum;j++)
		{
			if(table[j][indexArray[i]]!=-1 && inputPtr<input.size())
			{
				table[j][indexArray[i]]=(int)input[inputPtr];
				inputPtr++;
			}
		}
	}
	for(int i=0;i<table.size();i++)
	{
		for(int j=0;j<table[i].size();j++)
		{
			if(table[i][j]!=-1)
				output.push_back(char(table[i][j]-65+97));
		}
	}
}
else if(cipherWay=="vernam")
{
	//input="QK[N[JPQDSE`QTKH_MA_NK";
	vector<int >keyNum, inputNum;
	vector<string >keyBin, inputBin, outputBin;
	for(int i=0;i<input.size();i++)
	{
		inputNum.push_back(input[i]-65);
		inputBin.push_back(toBin(inputNum[i]));
	}
	for(int i=0;i<key.size();i++)
		keyNum.push_back(key[i]-65);
	for(int i=0;i<key.size();i++)
	{
		keyBin.push_back(toBin(keyNum[i]));
		int tmp=xorFunc(keyBin[i],inputBin[i]);
		outputBin.push_back(toBin(tmp));
		output.push_back(char(tmp+97));
	}
	//ptr to decode gradually
	int keyPtr=0;
	int inputPtr=key.size();
	while(output.size()!=input.size())
	{
		keyBin.push_back(outputBin[keyPtr]);
		int tmp=xorFunc(keyBin[keyBin.size()-1],inputBin[inputPtr]);
		outputBin.push_back(toBin(tmp));
		output.push_back(char(tmp+97));
		keyPtr++;
		inputPtr++;
	}
}
else if(cipherWay=="playfair")
{
	for(int i=0;i<key.size();i++)
		key[i]=key[i]-65+97;
	//replace j char to i
	for(int i=0;i<key.size();i++)
	{
		if(key[i]=='j')
			key[i]='i';
	}
	//remove duplicate key characters
	for(int i=0;i<key.size();i++)
	{
		for(int j=i-1;j>=0;j--)
		{
			if(key[j]==key[i])
			{
				key.erase(i,1);
				i--;
			}
		}
	}
	int rowCheck[26] = {0};
	for(int i=0;i<key.size();i++)
	{
		rowCheck[int(key[i])-97]=1;
	}
	rowCheck[9]=-1;//skip j col
	char table[5][5];
	int rnd=key.size()/5;
	int mod=key.size()%5;
	int keyPtr=0;
	//create table
	for(int i=0;i<rnd;i++)
	{
		for(int j=0;j<5;j++)
		{
			table[i][j]=key[keyPtr];
			keyPtr++;
		}
	}
	int rowCheckPtr=0;
	if(mod!=0)
	{
		for(int i=0;i<mod;i++)
		{
			table[rnd][i]=key[keyPtr];
			keyPtr++;
		}
		for(int i=mod;i<5;i++)
		{
			while(rowCheck[rowCheckPtr]!=0)
			{
				rowCheckPtr++;
			}
			table[rnd][i]=char(rowCheckPtr+97);
			rowCheckPtr++;
		}
		rnd++;
	}
	for(int i=rnd;i<5;i++)
	{
		for(int j=0;j<5;j++)
		{
			while(rowCheck[rowCheckPtr]!=0)
			{
				rowCheckPtr++;
			}
			table[i][j]=char(rowCheckPtr+97);
			rowCheckPtr++;
		}
	}
	//deal input to lower case
	for(int i=0;i<input.size();i++)
		input[i]=input[i]-65+97;
	//decryption
	for(int i=0;i<input.size();i=i+2)
	{
		vector<int >firstChar, secondChar;
		firstChar=lookTable(table,input[i]);
		secondChar=lookTable(table,input[i+1]);
		//in the same row
		if(firstChar[0]==secondChar[0])
		{
			if(firstChar[1]>0)
				output.push_back(table[firstChar[0]][firstChar[1]-1]);
			else
				output.push_back(table[firstChar[0]][4]);
			if(secondChar[1]>0)
				output.push_back(table[secondChar[0]][secondChar[1]-1]);
			else
				output.push_back(table[secondChar[0]][4]);

		}
		//in the same col
		else if(firstChar[1]==secondChar[1])
		{
			if(firstChar[0]>0)
				output.push_back(table[firstChar[0]-1][firstChar[1]]);
			else
				output.push_back(table[4][firstChar[1]]);
			if(secondChar[0]>0)
				output.push_back(table[secondChar[0]-1][secondChar[1]]);
			else
				output.push_back(table[4][secondChar[1]]);
		}
		//else
		else
		{
			output.push_back(table[firstChar[0]][secondChar[1]]);
			output.push_back(table[secondChar[0]][firstChar[1]]);
		}
	}
}
cout<<output<<endl;
}
