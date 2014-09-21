using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Runtime.InteropServices;

namespace CoolCard
{
    class IniFileOperator
    {
        //API��������

        [DllImport("kernel32")] //����0��ʾʧ��,��0Ϊ�ɹ� 
        private static extern long WritePrivateProfileString(string section, string key, string val, string filePath);

        [DllImport("kernel32")] //����ȡ���ַ����������ĳ���
        private static extern long GetPrivateProfileString(string section, string key, string def, StringBuilder retVal, int size, string filePath);


        // ��ini�ļ�

        public static  string ReadIniFile(string Section, string Key, string NoText, string iniFilePath) 
        {
            if (File.Exists(iniFilePath))
            {
                StringBuilder temp = new StringBuilder(1024);
                GetPrivateProfileString(Section, Key, NoText, temp, 1024, iniFilePath);
                return temp.ToString();
            }
            else
            {
                return String.Empty;
            }
        }


        // дini�ļ�

        public static  bool WriteIniFile(string Section, string Key, string Value, string iniFilePath)
        {
            if (File.Exists(iniFilePath))
            {
                long OpStation = WritePrivateProfileString(Section, Key, Value, iniFilePath);
                if (OpStation == 0)
                {
                    return false;
                }
                else
                {
                    return true;
                }
            }
            else 
            {
                return false;
            }
        }
    }
}
