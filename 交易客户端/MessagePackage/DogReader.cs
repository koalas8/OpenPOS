using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;

namespace CoolCard.MessagePackage
{
    public class DogReader
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
        /// 打卡ET199加密狗并读取里面的文件
        /// </summary>
        /// <param name="fileID">
        /// 	用于读取加密狗文件的加密狗程序
        /// </param>
        /// <returns>要读取的文件内容</returns>
        public string readET199(string fileID)
        {
            // 枚举ET199
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

            // 检查是否仅一个设备

            if (dwET199Count > 1)
            {
                return "1";
            }

            // 检查是否插入了加密狗
            if (dwET199Count < 1)
            {
                return "1";
            }

            // 打开 ET199
            dwRet = ETOpen(pET199);
            if (dwRet != 0)
            {
                return "1";
            }


            // 验证口令
            byte[] devPin = new byte[8] // 用户口令
            {
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38
            };
            dwRet = ETVerifyPin(pET199, devPin, 8, 0); // 验证用户口令
            if (dwRet != 0)
            {
                return "1";
            }

            byte[] pInBuffer = new byte[1] { 0x00 };
            uint dwInBufferSize = 0;

            byte[] pOutBuffer = new byte[1] { 0x00 };
            uint dwOutBufferSize = 0;
            if (fileID == "2001")
            {
                pOutBuffer = new byte[15] { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
                dwOutBufferSize = 15;
            }
            else if (fileID == "2002")
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
        /// 获取加密狗中的终端号
        /// </summary>
        /// <returns>8位终端号</returns>
        public string readTerminalNo()
        {
            string fileID = "2002";
            return this.readET199(fileID);
        }

        /// <summary>
        /// 获取加密狗中的商户号
        /// </summary>
        /// <returns>15位商户号</returns>
        public string readShopNo()
        {
            string fileID = "2001";
            return this.readET199(fileID);
        }

        /// <summary>
        /// 获取加密狗中的DES密钥
        /// </summary>
        /// <returns></returns>
        public string readDesKey()
        {
            string fileID = "2003";
            return this.readET199(fileID);
        }
    }
}
