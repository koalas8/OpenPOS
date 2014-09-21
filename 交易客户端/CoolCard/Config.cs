using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;

namespace CoolCard
{
    class Config
    {
        [DllImport("ET199_32.dll")]
        public static extern uint ETEnum(byte[] pETContextList, ref uint dwET199Count);

        [DllImport("ET199_32.dll")]
        public static extern uint ETOpen(byte[] pETContextList);

        [DllImport("ET199_32.dll")]
        public static extern uint ETClose(byte[] pETContextList);

        [DllImport("ET199_32.dll")]
        public static extern uint ETVerifyPin(byte[] pETContextList, byte[] pbPin, uint dwPinLen, uint dwPinType);


        [DllImport("ET199_32.dll")]
        public static extern uint ETChangePin(byte[] pETContextList, byte[] pbOldPin, uint dwOldPinLen, byte[] pbNewPin, uint dwNewPinLen, uint dwPinType, byte byPinTryCount);


        [DllImport("ET199_32.dll")]
        public static extern uint ETExecute(byte[] pETContextList, string lpszFileID, byte[] pInBuffer, uint dwInbufferSize, byte[] pOutBuffer, uint dwOutBufferSize, ref uint pdwBytesReturned);

        [DllImport("ET199_32.dll")]
        public static extern uint ETControl(byte[] pETContextList, uint dwCtlCode, byte[] pInBuffer, uint dwInbufferSize, byte[] pOutBuffer, uint dwOutBufferSize, ref uint pdwBytesReturned);

        [DllImport("ET199_32.dll")]
        public static extern uint ETCreateFile(byte[] pET199, string lpszFileID, uint dwFileSize, uint bFileType);

        [DllImport("ET199_32.dll")]
        public static extern uint ETWriteFile(byte[] pET199, string lpszFileID, uint dwOffset, byte[] pBuffer, uint dwBufferSize);

        [DllImport("ET199_32.dll")]
        public static extern uint ETGenRsaKey(byte[] pET199, uint wKeySize, uint dwE, byte[] lpszPubFileID, byte[] lpszPriFileID, byte[] pbPubKeyData, ref uint dwPubKeyDataSize, byte[] pbPriKeyData, ref uint dwPriKeyDataSize);


        uint dwET199Count = 0;
        uint dwRet = 0;
        uint pdwBytesReturned = 0;
        byte[] pET199 = new byte[56 * 1]; //sizeof(ET_CONTEXT)=56

        /// <summary>
        /// ��ET199���ܹ�����ȡ������ļ�
        /// </summary>
        /// <param name="fileID">
        /// 	���ڶ�ȡ���ܹ��ļ��ļ��ܹ�����
        /// </param>
        /// <returns>Ҫ��ȡ���ļ�����</returns>
        public string readET199(string fileID)
        {
            // ö��ET199
            dwRet = ETEnum(null, ref dwET199Count);
            if ((dwRet != 0xf0000004) && (dwRet != 0))  //0xF0000004 = ET_E_INSUFFICIENT_BUFFER
            {
                return "1";
            }
             pET199 = new byte[56 * dwET199Count]; //sizeof(ET_CONTEXT)=56

            dwRet = ETEnum(pET199, ref dwET199Count);
            if (dwRet != 0)
            {
                return "1";
            }

            // ����Ƿ��һ���豸

            if (dwET199Count > 1)
            {
                return "1";
            }

            // ����Ƿ�����˼��ܹ�
            if (dwET199Count < 1)
            {
                return "1";
            }

            // �� ET199
            dwRet = ETOpen(pET199);
            if (dwRet != 0)
            {
                return "1";
            }


            // ��֤����
            byte[] devPin = new byte[8] // �û�����
            {
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38
            };
            dwRet = ETVerifyPin(pET199, devPin, 8, 0); // ��֤�û�����
            if (dwRet != 0)
            {
                return "1";
            }

            byte[] pInBuffer = new byte[1] { 0x00 };
            uint dwInBufferSize = 0;

            byte[] pOutBuffer = new byte[1]{0x00};
            uint dwOutBufferSize = 0;
            if (fileID == "2001")
            {
                pOutBuffer = new byte[15] { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
                dwOutBufferSize = 15;
            }
            else if(fileID == "2002")
            {
                pOutBuffer = new byte[8] { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
                dwOutBufferSize = 8;
            }
            else if (fileID == "2003")
            {
                pOutBuffer = new byte[8] { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
                dwOutBufferSize = 8;
            }

            dwRet = ETExecute(pET199, fileID, pInBuffer, dwInBufferSize, pOutBuffer, dwOutBufferSize, ref pdwBytesReturned);
            if (dwRet != 0)
            {
                return "1";
            }

            ETClose(pET199);
            return System.Text.Encoding.Default.GetString(pOutBuffer);

        }

        /// <summary>
        /// ��ȡ���ܹ��е��ն˺�
        /// </summary>
        /// <returns>8λ�ն˺�</returns>
        public string getTerminalNo()
        {                        
            string fileID = "2002";
            return this.readET199(fileID);
        }

        /// <summary>
        /// ��ȡ���ܹ��е��̻���
        /// </summary>
        /// <returns>15λ�̻���</returns>
        public string getShopNo()
        {
            string fileID = "2001";
            return this.readET199(fileID);
        }

        /// <summary>
        /// ��ȡ���ܹ��е�DES��Կ
        /// </summary>
        /// <returns></returns>
        public string getDesKey()
        {
            string fileID = "2003";
            return this.readET199(fileID);
        }

        
         /// <summary>
         /// ��ȡȡ�����׼��ļ�ֵ
         /// </summary>
         /// <returns></returns>
         public string getCancelKeyValue()
         {
             return "27";
         }

        /// <summary>
        /// ��ȡ������ļ�ֵ 
        /// </summary>
        /// <returns></returns>
        public string getClearKeyValue()
        {
            return "8";
        }
        
        
        /// <summary>
        /// ��ȡ����������Ŀ¼
        /// </summary>
        /// <returns></returns>
        public static String GetAppRootPath()
        {
        	return Environment.CurrentDirectory;
        }
        
        /// <summary>
        /// ��ȡ���������ļ��е�ֵ
        /// </summary>
        /// <param name="group">�����ļ��е���</param>
        /// <param name="key">Ҫ��ȡֵ��key</param>
        /// <param name="defaultValue">��������ļ���û���ҵ�Ҫ��ȡ�Ĳ������򷵻ش�ֵ</param>
        /// <param name="configFile">�����ļ���·��</param>
        /// <returns></returns>
        public static String GetConfig(String group, String key, String defaultValue, String configFile)
        {
        	String value = IniFileOperator.ReadIniFile(group, key, defaultValue, configFile);
        	return value;
        }
        
        /// <summary>
        /// ��ȡ���������ļ��е�ֵ(Ĭ�������ļ�Ϊ����Ŀ¼�µ�config.cfg)
        /// </summary>
        /// <param name="group">�����ļ��е���</param>
        /// <param name="key">Ҫ��ȡֵ��key</param>
        /// <param name="defaultValue">��������ļ���û���ҵ�Ҫ��ȡ�Ĳ������򷵻ش�ֵ</param>
        /// <returns></returns>
        public static String GetConfig(String group, String key, String defaultValue)
        {
        	String configFile = GetAppRootPath() + "/config.cfg";
        	return GetConfig(group, key, defaultValue, configFile);
        }
        
        /// <summary>
        /// ��ȡ���������ļ��е�ֵ(Ĭ�������ļ�Ϊ����Ŀ¼�µ�config.cfg;��������ļ���û���ҵ�Ҫ��ȡ�Ĳ������򷵻�"")
        /// </summary>
        /// <param name="group">�����ļ��е���</param>
        /// <param name="key">Ҫ��ȡֵ��key</param>
        /// <returns></returns>
        public static String GetConfig(String group, String key)
        {
        	return GetConfig(group, key, "");
        }
    }
}
