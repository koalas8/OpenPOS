using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;

namespace CoolCard
{

/**
 * //////使用方法
 * private void button1_Click(object sender, EventArgs e)
 * {
 *      LPTControls.LPTControls lpt = new LPTControls.LPTControls();
 *      string mycommanglines = System.IO.File.ReadAllText("print.txt");//print.txt里写了条码机的命令
 *      lpt.Open();
 *      lpt.Write(mycommanglines);
 *      lpt.Close();
 * }
*/
    class LptPrinter
    {
        [StructLayout(LayoutKind.Sequential)]
        private struct OVERLAPPED
        {
            int Internal;
            int InternalHigh;
            int Offset;
            int Offsethigh;
            int hEvent;
        }

        [DllImport("kernel32.dll")]
        private static extern int CreateFile(string lpFileName,
            uint dwDesiredAddress,
            int dwShareMode,
            int lpSecurityAttributes,
            int dwCreationDisposition,
            int dwFlagsAndAttributes,
            int hTemplateFile);

        [DllImport("kernel32.dll")]
        private static extern bool WriteFile(int hFile,
            byte[] lpBuffer,
            int nNumberOfBytesToWriter,
            out int lpNumberOfBytesWriten,
            out OVERLAPPED lpOverLapped);

        [DllImport("kernel32.dll")]
        private static extern bool CloseHandle(int hObject);
        private int iHandle;
        
        //打开LPT 端口
        public bool Open()
        {
            iHandle = CreateFile("lpt1", 0x40000000, 0, 0, 3, 0, 0);
            if (iHandle != -1)
            {
                return true;
            }
            else 
            {
                return false;
            }
        }

        //打印函数，参数为打印机的命令或者其它文本
        public bool Write(string myString)
        {
            if (iHandle != 1)
            {
                int i;
                OVERLAPPED x;
                byte[] myByte = System.Text.Encoding.Default.GetBytes(myString);
                return WriteFile(iHandle, myByte, myByte.Length, out i, out x);
            }
            else
            {
                throw new Exception("端口未打开!");
            }
        }

        //关闭打印端口
        public bool Close()
        {
            return CloseHandle(iHandle);
        }
    }
}
