/*
 *  程序功能： 
 *      1.通过ET199生成私钥和公钥，并将公钥导出到文件
 *      2.将商户号和终端号写入到ET199中
 * 
 *  各文件在ET199中的ID:
 *      1.公钥文件: 1001
 *      2.私钥文件: 1002
 *      3.商户号文件: 3001
 *      4.终端号文件: 3002
 *      5.读取商户号的程序文件: 2001
 *      6.读取终端号的程序文件: 2002
 *      
 */

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using Npgsql;

namespace WriteKeys
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }


       

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
        public static extern uint ETCreateFile(byte[] pET199, string  lpszFileID, uint dwFileSize, uint bFileType);

        [DllImport("ET199_32.dll")]
        public static extern uint ETWriteFile(byte[] pET199, string lpszFileID, uint dwOffset, byte[] pBuffer, uint dwBufferSize);

        [DllImport("ET199_32.dll")]
        public static extern uint ETChangeDir(byte[] pET199, string path);

        [DllImport("ET199_32.dll")]
        public static extern uint ETEraseDir(byte[] pET199, string path);

        [DllImport("ET199_32.dll")]
        public static extern uint ETCreateDir(byte[] pET199, string path, uint dwDirSize, uint dwDirFlags);

        [DllImport("ET199_32.dll")]
        public static extern uint ETGenRsaKey(byte[] pET199, uint wKeySize, uint dwE, byte[] lpszPubFileID, byte[] lpszPriFileID, byte[] pbPubKeyData, ref uint dwPubKeyDataSize, byte[] pbPriKeyData, ref uint dwPriKeyDataSize);

        // 显示当前进度
        private void showState(string msg)   
        {
            this.toolStripStatusLabel2.Text = msg;
            this.statusStrip1.Refresh();
        }

        private void showError(uint msg)
        {
            this.showState("错误: 0x" + msg.ToString("X"));
            MessageBox.Show("错误: 0x" + msg.ToString("X"));
            this.showState("就绪");
            this.EnableControls();
        }

        private void showError(string msg)
        {
            this.showState("错误:" + msg);
            MessageBox.Show("错误:" + msg);
            this.showState("就绪");
            this.EnableControls();
        }


        private string ET199Flash(byte[] pET199)
        {
            uint dwRet = 0;
            byte[] pOutBuffer = new byte[1];
            uint pwdOutBufferSize = 0;
            dwRet = ETControl(pET199, 3, new byte[1] { 0x05 }, 1, pOutBuffer, 0, ref pwdOutBufferSize);
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            return "0";
        }

        /// <summary>
        /// 在ET199设备中创建文件
        /// </summary>
        /// <param name="pET199">枚举出的ET199设备</param>
        /// <param name="fileID">文件名，4个字符</param>
        /// <param name="fileSize">文件的大小</param>
        /// <param name="fileType">文件类型: 
        ///        #define FILE_TYPE_EXE 0 /** 可执行文件*/ 
        ///        #define FILE_TYPE_DATA 1 /** 数据文件*/ 
        ///        #define FILE_TYPE_RSA_PUBLIC 2 /** RSA 公钥文件*/ 
        ///        #define FILE_TYPE_RSA_PRIVATE 3 /** RSA 私钥文件*/ 
        ///        #define FILE_TYPE_INTERNAL_EXE 4 /** 可执行文件（不可读写）*/
        /// </param>
        /// <returns>"0"-成功；其它-错误信息</returns>
        private string createET199File(byte[] pET199, string fileID, uint fileSize, uint fileType)
        {
            uint dwRet = 0;
            dwRet = ETCreateFile(pET199, fileID, fileSize, fileType);
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            else
            {
                return "0";
            }
            
        }

        /// <summary>
        ///  向创建的ET199文件中写入文件内容 
        /// </summary>
        /// <param name="pET199">枚举出的ET199设备</param>
        /// <param name="fileID">文件名，4个字符</param>
        /// <param name="offset">写入时偏移</param>
        /// <param name="fileContent">文件内容，byte[]类型</param>
        /// <param name="fileSize">文件大小</param>
        /// <returns>"0"-成功；其它-错误信息</returns>
        private string  writeET199File(byte[] pET199, string fileID, uint offset, byte[] fileContent, uint fileSize)
        {
            uint dwRet = 0;
            dwRet = ETWriteFile(pET199, fileID, 0, fileContent, fileSize);
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            else 
            {
                return "0";
            }
        }

        /// <summary>
        /// 验证开发商口令
        /// </summary>
        /// <param name="pET199"></param>
        /// <returns></returns>
        private string verifyDevPin(byte[] pET199)
        {
            uint dwRet = 0;
            byte[] devPin = new byte[24] // 开发商口令
            {
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38
            };
            dwRet = ETVerifyPin(pET199, devPin, 24, 1); // 验证开发商口令
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            return "0";
            
        }

        /// <summary>
        /// 验证开用户口令
        /// </summary>
        /// <param name="pET199"></param>
        /// <returns></returns>
        private string verifyUserPin(byte[] pET199)
        {
            uint dwRet = 0;
            byte[] devPin = new byte[8] // 开发商口令
            {
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38
            };
            dwRet = ETVerifyPin(pET199, devPin, 8, 0); // 验证开发商口令
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            return "0";

        }


        /// <summary>
        /// 重建ET199文件系统。
        /// 过程：切换到根目录，清除根目录，创建根目录
        /// </summary>
        /// <param name="pET199"></param>
        /// <returns></returns>
        private string rebuildFileSystem(byte[] pET199)
        {
            uint dwRet = 0;            

            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            dwRet = ETChangeDir(pET199, @"\");
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            this.verifyDevPin(pET199);
            dwRet = ETEraseDir(pET199, "");
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            dwRet = ETCreateDir(pET199, "", 0, 0);
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            return "0";
        }

        /// <summary>
        /// 检查表单填写是否正确
        /// 检查表单填写的文件是否存在
        /// </summary>
        /// <returns>表单正确返回 true, 否则返回false</returns>
        private bool CheckForm()
        {
            if (  this.txtMerchantNo.Text.Trim() == ""
               || this.txtTerminalNo.Text.Trim() == ""
               || this.txttDESReaderPgm.Text.Trim () == ""
               || this.txtMerchantNumReaderPgm.Text.Trim() == ""
               || this.txtTerminalNumReaderPgm.Text.Trim() == ""
                )
            {
                MessageBox.Show("请完整填写信息!");
                return false;
            }


            if (this.txtMerchantNo.Text.Trim().Length != 15)
            {
                MessageBox.Show("商户号为15位!");
                return false;
            }

            if (this.txtTerminalNo.Text.Trim().Length != 8)
            {
                MessageBox.Show("终端号为8位!");
                return false;
            }

            if (!System.IO.File.Exists(this.txtMerchantNumReaderPgm.Text.Trim()))
            {
                this.showError("文件[商户号读取程序]不存在!");
                return false;
            }
            if (!System.IO.File.Exists(this.txtTerminalNumReaderPgm.Text.Trim()))
            {
                this.showError("文件[终端号读取程序]不存在!");
                return false;
            }
            if(!System.IO.File.Exists(this.txttDESReaderPgm.Text.Trim()))
            {
                this.showError("文件[密钥读取程序]不存在!");
                return false;
            }
            return true;
        }

        /// <summary>
        /// 禁用控件，防止用户误操作
        /// </summary>
        private void DisableControls()
        {
            this.button1.Enabled = false;
            this.btnBrowseMerchNumReader.Enabled = false;
            this.btnBrowseTermNumReader.Enabled = false;
            this.txtMerchantNo.ReadOnly = true;
            this.txtTerminalNo.ReadOnly = true;
        }

        /// <summary>
        /// 启用控件
        /// </summary>
        private void EnableControls()
        {
            this.button1.Enabled = true;
            this.btnBrowseMerchNumReader.Enabled = true;
            this.btnBrowseTermNumReader.Enabled = true;
            this.txtMerchantNo.ReadOnly = false;
            this.txtTerminalNo.ReadOnly = false;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (this.CheckForm() == false) return; // 检查表单是否正确

            this.DisableControls(); // 禁用相关控件，防止误操作
            
            String desKey = desKey = this.GetRnd(8, true, true, true, false, "");
            var server = CoolCard.IniFileOperator.ReadIniFile("NET", "host", "127.0.0.1", Environment.CurrentDirectory + "/conf.cfg");
            String connString = "Server=" + server + ";Port=5432;User Id=pgsql;Password=123456;Database=jf_card;";
            NpgsqlConnection conn = new NpgsqlConnection(connString);
            conn.Open();
            NpgsqlCommand command = new NpgsqlCommand(String.Format("SELECT COUNT(*) FROM shop_info WHERE shop_no = '{0}'", this.txtMerchantNo .Text ), conn);
            long count = (long)command.ExecuteScalar();
            if(count == 0)
            {
            	MessageBox.Show("此商户不存在");
            	this.EnableControls();
            	return;
            }
            else
            {
            	command.CommandText = String.Format("SELECT COUNT(*) FROM terminal_info WHERE terminal_no='{0}'", this.txtTerminalNo.Text );
            	count = (long)command .ExecuteScalar();
            	if (count == 0)
            	{
            		MessageBox.Show("此终端不存在");
            		this.EnableControls();
            		return;
            	}
            }
            command .CommandText = String.Format("SELECT COUNT(*) FROM terminal_info WHERE (des_key<>'' OR des_key<>NULL) AND terminal_no='" + this.txtTerminalNo.Text + "'");
            count = (long)command .ExecuteScalar();
            if (count > 0)
            {
            	if(MessageBox.Show("此终端号已经设置密钥，是否更新?", "", MessageBoxButtons .OKCancel) == DialogResult .OK)
            	{            		
            		command.CommandText = String.Format("UPDATE terminal_info SET des_key='{0}' WHERE terminal_no='{1}'", desKey , this.txtTerminalNo.Text);
            		command.ExecuteNonQuery();
            	}
            	else
            	{
            		this.EnableControls();
            		return;
            	}
            }
			else
			{
            	command.CommandText = String.Format("UPDATE terminal_info SET des_key='{0}' WHERE terminal_no='{1}'", desKey , this.txtTerminalNo.Text);
            	command.ExecuteNonQuery();
			}            		

            string merchantNumReaderFile = this.txtMerchantNumReaderPgm.Text.Trim();  // 读取商户号的程序,写入到ET199中用
            string terminalNumReaderFile = this.txtTerminalNumReaderPgm.Text.Trim();  // 读取终端号的程序,写入到ET199中用
            string tDESReaderFile = this.txttDESReaderPgm.Text.Trim(); // 读取密钥文件的程序,写入到ET199中用      
            
            uint dwET199Count = 0;
            uint dwRet = 0;
            uint merchantNumReaderFileLength = 0; // 读取商户号的程序大小(bytes)
            uint terminalNumReaderFileLength = 0; // 读取终端号的程序大小(bytes)
            uint tDESReaderFileLength = 0; // 读取密钥的程序大小(bytes)

            System.IO.FileInfo fInfo = new System.IO.FileInfo(merchantNumReaderFile);
            merchantNumReaderFileLength = (uint)fInfo.Length;  // 获取读取商户号的程序大小
            fInfo = new System.IO.FileInfo(terminalNumReaderFile);
            terminalNumReaderFileLength = (uint)fInfo.Length;  // 获取读取终端号的程序大小
            fInfo = new System.IO.FileInfo(tDESReaderFile);
            tDESReaderFileLength = (uint)fInfo.Length;  // 读取密钥的程序大小


            // 枚举ET199
            this.showState("正在查找设备...");
            dwRet = ETEnum(null, ref dwET199Count);
            if ((dwRet != 0xf0000004) && (dwRet != 0))  //0xF0000004 = ET_E_INSUFFICIENT_BUFFER
            {
                this.showError("没有找到设备,请插入设备后重试!");
                return;
            }

            byte[] pET199 = new byte[56 * dwET199Count]; //sizeof(ET_CONTEXT)=56

            dwRet = ETEnum(pET199, ref dwET199Count);
            if (dwRet != 0)
            {
                this.showError(dwRet);
                return;
            }

            // 检查是否仅一个设备
            
            if (dwET199Count > 1)
            {
                this.showError("找到多个设备,请移除多余设备后重试!");
            }

            // 打开 ET199
            this.showState("打开设备...");
            dwRet = ETOpen(pET199);
            if (dwRet != 0)
            {
                this.showError(dwRet);
                return;
            }


            // 重建文件系统
            this.showState("设备初始化...");
            string result = this.rebuildFileSystem(pET199);
            if (result != "0")
            {
                this.showError(result);
                return;
            }

            string merchantNumReaderFileID = "2001"; // 读取商户号的程序ID
            string terminalNumReaderFileID = "2002"; // 读取终端号的程序ID
			string tDESReaderFileID = "2003"; // 读取DES密钥的程序ID
            string merchantNumFileID = "3001"; // 商户号文件ID
            string terminalNumFileID = "3002";  // 终端号文件ID
            string tDesFileID = "3003"; // 3DES密钥文件ID
                  
            this.verifyDevPin(pET199);  // 创建文件前要验证开发商口令

            this.showState("创建文件...");
            result = createET199File(pET199, merchantNumFileID, 15, 1); // 创建商户号文件
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            result = writeET199File(pET199, merchantNumFileID, 0, System.Text.Encoding.Default.GetBytes(this.txtMerchantNo.Text.ToString().Trim()), 15); // 写入商户号
            if (result != "0")
            {
                this.showError(result);
                return;
            }


            result = createET199File(pET199, terminalNumFileID, 8, 1); // 创建终端号文件
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            result = writeET199File(pET199, terminalNumFileID, 0, System.Text.Encoding.Default.GetBytes(this.txtTerminalNo.Text.ToString().Trim()), 8); //写入终端号
            if (result != "0")
            {
                this.showError(result);
                return;
            }


            result = createET199File(pET199, tDesFileID, 8, 1); // 创建3DES密钥文件
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            result = writeET199File(pET199, tDesFileID, 0, System.Text.Encoding.Default.GetBytes(desKey), 8); // 写入密钥文件
            if (result != "0")
            {
                this.showError(result);
                return;
            }

            
            result = createET199File(pET199, merchantNumReaderFileID, merchantNumReaderFileLength, 0); // 创建商户号读取程序
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            byte[] tmp_buffer = new byte[merchantNumReaderFileLength];
            new System.IO.FileStream(merchantNumReaderFile, System.IO.FileMode.Open, System.IO.FileAccess.Read).Read(tmp_buffer, 0, (int)merchantNumReaderFileLength);
            result = writeET199File(pET199, merchantNumReaderFileID, 0, tmp_buffer, merchantNumReaderFileLength); //写入商户号读取程序
            if (result != "0")
            {
                this.showError(result);
                return;
            }


            result = createET199File(pET199, terminalNumReaderFileID, terminalNumReaderFileLength, 0); // 创建终端号读取程序
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            tmp_buffer = new byte[terminalNumReaderFileLength];
            new System.IO.FileStream(terminalNumReaderFile, System.IO.FileMode.Open, System.IO.FileAccess.Read).Read(tmp_buffer, 0, (int)terminalNumReaderFileLength);
            result = writeET199File(pET199, terminalNumReaderFileID, 0, tmp_buffer, terminalNumReaderFileLength); //写入终端号读取程序
            if (result != "0")
            {
                this.showError(result);
                return;
            }

            result = createET199File(pET199, tDESReaderFileID, tDESReaderFileLength, 0); // 创建密钥读取程序
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            tmp_buffer = new byte[tDESReaderFileLength];
            new System.IO.FileStream(tDESReaderFile, System.IO.FileMode.Open, System.IO.FileAccess.Read).Read(tmp_buffer, 0, (int)tDESReaderFileLength);
            result = writeET199File(pET199, tDESReaderFileID, 0, tmp_buffer, tDESReaderFileLength); //写入密钥读取程序
            if (result != "0")
            {
                this.showError(result);
                return;
            }            

            // 关闭设备
            dwRet = ETClose(pET199);
            if (dwRet != 0)
            {
                this.showError(dwRet);
                return;
            }


            this.showState("写入完成");
            MessageBox.Show("写入完成");
            this.showState("就绪");
            this.EnableControls();
        }
       
        private void Form1_Load(object sender, EventArgs e)
        {
            this.UpdateLengthInfo();
        }

        /// <summary>
        /// 更新状态栏的表单长度信息
        /// </summary>
        private void UpdateLengthInfo()
        {
            this.toolStripStatusLabel_Merchant_length.Text = this.txtMerchantNo.Text.Trim().Length.ToString();
            this.toolStripStatusLabel_Terminal_length.Text = this.txtTerminalNo.Text.Trim().Length.ToString();
        }

        private void txtMerchantNo_TextChanged(object sender, EventArgs e)
        {
            this.UpdateLengthInfo();
        }

        private void txtTerminalNo_TextChanged(object sender, EventArgs e)
        {
            this.UpdateLengthInfo();
        }

        private void btnBrowseMerchNumReader_Click(object sender, EventArgs e)
        {
            this.openFileDialog1.CheckFileExists = true;
            this.openFileDialog1.CheckPathExists = true;
            this.openFileDialog1.DefaultExt = ".bin";
            this.openFileDialog1.FileName = "";
            this.openFileDialog1.Filter = "ET199程序(*.bin)|*.bin";
            this.openFileDialog1.Multiselect = false;
            if (this.openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                this.txtMerchantNumReaderPgm.Text = this.openFileDialog1.FileName;
            }
        }

        private void btnBrowseTermNumReader_Click(object sender, EventArgs e)
        {
            this.openFileDialog1.CheckFileExists = true;
            this.openFileDialog1.CheckPathExists = true;
            this.openFileDialog1.DefaultExt = ".bin";
            this.openFileDialog1.FileName = "";
            this.openFileDialog1.Filter = "ET199程序(*.bin)|*.bin";
            this.openFileDialog1.Multiselect = false;
            if (this.openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                this.txtTerminalNumReaderPgm.Text = this.openFileDialog1.FileName;
            }
        }

        private void txt3DES_TextChanged(object sender, EventArgs e)
        {
            this.UpdateLengthInfo();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.openFileDialog1.CheckFileExists = true;
            this.openFileDialog1.CheckPathExists = true;
            this.openFileDialog1.DefaultExt = ".bin";
            this.openFileDialog1.FileName = "";
            this.openFileDialog1.Filter = "ET199程序(*.bin)|*.bin";
            this.openFileDialog1.Multiselect = false;
            if (this.openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                this.txttDESReaderPgm.Text = this.openFileDialog1.FileName;
            }
        }
        
        /// <summary>
        /// 生成随机字符串
        /// </summary>
        /// <param name="length">目标字符串的长度</param>
        /// <param name="useNum">是否包含数字，1=包含，默认为包含</param>
        /// <param name="useLow">是否包含小写字母，1=包含，默认为包含</param>
        /// <param name="useUpp">是否包含大写字母，1=包含，默认为包含</param>
        /// <param name="useSpe">是否包含特殊字符，1=包含，默认为不包含</param>
        /// <param name="custom">要包含的自定义字符，直接输入要包含的字符列表</param>
        /// <returns>指定长度的随机字符串</returns>
        private string GetRnd(int length, bool useNum, bool useLow, bool useUpp, bool useSpe, string custom)
        {
            byte[] b = new byte[4];
            new System.Security.Cryptography.RNGCryptoServiceProvider().GetBytes(b);
            Random r = new Random(BitConverter.ToInt32(b, 0));
            string s = null, str = custom;

            if (useNum == true) { str += "0123456789"; }
            if (useLow == true) { str += "abcdefghijklmnopqrstuvwxyz"; }
            if (useUpp == true) { str += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; }
            if (useSpe == true) { str += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"; }

            for (int i = 0; i < length; i++)
            {
                s += str.Substring(r.Next(0, str.Length - 1), 1);
            }

            return s;
        }


    }
}