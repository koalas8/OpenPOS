/*
 *  �����ܣ� 
 *      1.ͨ��ET199����˽Կ�͹�Կ��������Կ�������ļ�
 *      2.���̻��ź��ն˺�д�뵽ET199��
 * 
 *  ���ļ���ET199�е�ID:
 *      1.��Կ�ļ�: 1001
 *      2.˽Կ�ļ�: 1002
 *      3.�̻����ļ�: 3001
 *      4.�ն˺��ļ�: 3002
 *      5.��ȡ�̻��ŵĳ����ļ�: 2001
 *      6.��ȡ�ն˺ŵĳ����ļ�: 2002
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

        // ��ʾ��ǰ����
        private void showState(string msg)   
        {
            this.toolStripStatusLabel2.Text = msg;
            this.statusStrip1.Refresh();
        }

        private void showError(uint msg)
        {
            this.showState("����: 0x" + msg.ToString("X"));
            MessageBox.Show("����: 0x" + msg.ToString("X"));
            this.showState("����");
            this.EnableControls();
        }

        private void showError(string msg)
        {
            this.showState("����:" + msg);
            MessageBox.Show("����:" + msg);
            this.showState("����");
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
        /// ��ET199�豸�д����ļ�
        /// </summary>
        /// <param name="pET199">ö�ٳ���ET199�豸</param>
        /// <param name="fileID">�ļ�����4���ַ�</param>
        /// <param name="fileSize">�ļ��Ĵ�С</param>
        /// <param name="fileType">�ļ�����: 
        ///        #define FILE_TYPE_EXE 0 /** ��ִ���ļ�*/ 
        ///        #define FILE_TYPE_DATA 1 /** �����ļ�*/ 
        ///        #define FILE_TYPE_RSA_PUBLIC 2 /** RSA ��Կ�ļ�*/ 
        ///        #define FILE_TYPE_RSA_PRIVATE 3 /** RSA ˽Կ�ļ�*/ 
        ///        #define FILE_TYPE_INTERNAL_EXE 4 /** ��ִ���ļ������ɶ�д��*/
        /// </param>
        /// <returns>"0"-�ɹ�������-������Ϣ</returns>
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
        ///  �򴴽���ET199�ļ���д���ļ����� 
        /// </summary>
        /// <param name="pET199">ö�ٳ���ET199�豸</param>
        /// <param name="fileID">�ļ�����4���ַ�</param>
        /// <param name="offset">д��ʱƫ��</param>
        /// <param name="fileContent">�ļ����ݣ�byte[]����</param>
        /// <param name="fileSize">�ļ���С</param>
        /// <returns>"0"-�ɹ�������-������Ϣ</returns>
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
        /// ��֤�����̿���
        /// </summary>
        /// <param name="pET199"></param>
        /// <returns></returns>
        private string verifyDevPin(byte[] pET199)
        {
            uint dwRet = 0;
            byte[] devPin = new byte[24] // �����̿���
            {
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38
            };
            dwRet = ETVerifyPin(pET199, devPin, 24, 1); // ��֤�����̿���
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            return "0";
            
        }

        /// <summary>
        /// ��֤���û�����
        /// </summary>
        /// <param name="pET199"></param>
        /// <returns></returns>
        private string verifyUserPin(byte[] pET199)
        {
            uint dwRet = 0;
            byte[] devPin = new byte[8] // �����̿���
            {
                0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38
            };
            dwRet = ETVerifyPin(pET199, devPin, 8, 0); // ��֤�����̿���
            if (dwRet != 0)
            {
                return dwRet.ToString("X");
            }
            return "0";

        }


        /// <summary>
        /// �ؽ�ET199�ļ�ϵͳ��
        /// ���̣��л�����Ŀ¼�������Ŀ¼��������Ŀ¼
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
        /// ������д�Ƿ���ȷ
        /// ������д���ļ��Ƿ����
        /// </summary>
        /// <returns>����ȷ���� true, ���򷵻�false</returns>
        private bool CheckForm()
        {
            if (  this.txtMerchantNo.Text.Trim() == ""
               || this.txtTerminalNo.Text.Trim() == ""
               || this.txttDESReaderPgm.Text.Trim () == ""
               || this.txtMerchantNumReaderPgm.Text.Trim() == ""
               || this.txtTerminalNumReaderPgm.Text.Trim() == ""
                )
            {
                MessageBox.Show("��������д��Ϣ!");
                return false;
            }


            if (this.txtMerchantNo.Text.Trim().Length != 15)
            {
                MessageBox.Show("�̻���Ϊ15λ!");
                return false;
            }

            if (this.txtTerminalNo.Text.Trim().Length != 8)
            {
                MessageBox.Show("�ն˺�Ϊ8λ!");
                return false;
            }

            if (!System.IO.File.Exists(this.txtMerchantNumReaderPgm.Text.Trim()))
            {
                this.showError("�ļ�[�̻��Ŷ�ȡ����]������!");
                return false;
            }
            if (!System.IO.File.Exists(this.txtTerminalNumReaderPgm.Text.Trim()))
            {
                this.showError("�ļ�[�ն˺Ŷ�ȡ����]������!");
                return false;
            }
            if(!System.IO.File.Exists(this.txttDESReaderPgm.Text.Trim()))
            {
                this.showError("�ļ�[��Կ��ȡ����]������!");
                return false;
            }
            return true;
        }

        /// <summary>
        /// ���ÿؼ�����ֹ�û������
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
        /// ���ÿؼ�
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
            if (this.CheckForm() == false) return; // �����Ƿ���ȷ

            this.DisableControls(); // ������ؿؼ�����ֹ�����
            
            String desKey = desKey = this.GetRnd(8, true, true, true, false, "");
            var server = CoolCard.IniFileOperator.ReadIniFile("NET", "host", "127.0.0.1", Environment.CurrentDirectory + "/conf.cfg");
            String connString = "Server=" + server + ";Port=5432;User Id=pgsql;Password=123456;Database=jf_card;";
            NpgsqlConnection conn = new NpgsqlConnection(connString);
            conn.Open();
            NpgsqlCommand command = new NpgsqlCommand(String.Format("SELECT COUNT(*) FROM shop_info WHERE shop_no = '{0}'", this.txtMerchantNo .Text ), conn);
            long count = (long)command.ExecuteScalar();
            if(count == 0)
            {
            	MessageBox.Show("���̻�������");
            	this.EnableControls();
            	return;
            }
            else
            {
            	command.CommandText = String.Format("SELECT COUNT(*) FROM terminal_info WHERE terminal_no='{0}'", this.txtTerminalNo.Text );
            	count = (long)command .ExecuteScalar();
            	if (count == 0)
            	{
            		MessageBox.Show("���ն˲�����");
            		this.EnableControls();
            		return;
            	}
            }
            command .CommandText = String.Format("SELECT COUNT(*) FROM terminal_info WHERE (des_key<>'' OR des_key<>NULL) AND terminal_no='" + this.txtTerminalNo.Text + "'");
            count = (long)command .ExecuteScalar();
            if (count > 0)
            {
            	if(MessageBox.Show("���ն˺��Ѿ�������Կ���Ƿ����?", "", MessageBoxButtons .OKCancel) == DialogResult .OK)
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

            string merchantNumReaderFile = this.txtMerchantNumReaderPgm.Text.Trim();  // ��ȡ�̻��ŵĳ���,д�뵽ET199����
            string terminalNumReaderFile = this.txtTerminalNumReaderPgm.Text.Trim();  // ��ȡ�ն˺ŵĳ���,д�뵽ET199����
            string tDESReaderFile = this.txttDESReaderPgm.Text.Trim(); // ��ȡ��Կ�ļ��ĳ���,д�뵽ET199����      
            
            uint dwET199Count = 0;
            uint dwRet = 0;
            uint merchantNumReaderFileLength = 0; // ��ȡ�̻��ŵĳ����С(bytes)
            uint terminalNumReaderFileLength = 0; // ��ȡ�ն˺ŵĳ����С(bytes)
            uint tDESReaderFileLength = 0; // ��ȡ��Կ�ĳ����С(bytes)

            System.IO.FileInfo fInfo = new System.IO.FileInfo(merchantNumReaderFile);
            merchantNumReaderFileLength = (uint)fInfo.Length;  // ��ȡ��ȡ�̻��ŵĳ����С
            fInfo = new System.IO.FileInfo(terminalNumReaderFile);
            terminalNumReaderFileLength = (uint)fInfo.Length;  // ��ȡ��ȡ�ն˺ŵĳ����С
            fInfo = new System.IO.FileInfo(tDESReaderFile);
            tDESReaderFileLength = (uint)fInfo.Length;  // ��ȡ��Կ�ĳ����С


            // ö��ET199
            this.showState("���ڲ����豸...");
            dwRet = ETEnum(null, ref dwET199Count);
            if ((dwRet != 0xf0000004) && (dwRet != 0))  //0xF0000004 = ET_E_INSUFFICIENT_BUFFER
            {
                this.showError("û���ҵ��豸,������豸������!");
                return;
            }

            byte[] pET199 = new byte[56 * dwET199Count]; //sizeof(ET_CONTEXT)=56

            dwRet = ETEnum(pET199, ref dwET199Count);
            if (dwRet != 0)
            {
                this.showError(dwRet);
                return;
            }

            // ����Ƿ��һ���豸
            
            if (dwET199Count > 1)
            {
                this.showError("�ҵ�����豸,���Ƴ������豸������!");
            }

            // �� ET199
            this.showState("���豸...");
            dwRet = ETOpen(pET199);
            if (dwRet != 0)
            {
                this.showError(dwRet);
                return;
            }


            // �ؽ��ļ�ϵͳ
            this.showState("�豸��ʼ��...");
            string result = this.rebuildFileSystem(pET199);
            if (result != "0")
            {
                this.showError(result);
                return;
            }

            string merchantNumReaderFileID = "2001"; // ��ȡ�̻��ŵĳ���ID
            string terminalNumReaderFileID = "2002"; // ��ȡ�ն˺ŵĳ���ID
			string tDESReaderFileID = "2003"; // ��ȡDES��Կ�ĳ���ID
            string merchantNumFileID = "3001"; // �̻����ļ�ID
            string terminalNumFileID = "3002";  // �ն˺��ļ�ID
            string tDesFileID = "3003"; // 3DES��Կ�ļ�ID
                  
            this.verifyDevPin(pET199);  // �����ļ�ǰҪ��֤�����̿���

            this.showState("�����ļ�...");
            result = createET199File(pET199, merchantNumFileID, 15, 1); // �����̻����ļ�
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            result = writeET199File(pET199, merchantNumFileID, 0, System.Text.Encoding.Default.GetBytes(this.txtMerchantNo.Text.ToString().Trim()), 15); // д���̻���
            if (result != "0")
            {
                this.showError(result);
                return;
            }


            result = createET199File(pET199, terminalNumFileID, 8, 1); // �����ն˺��ļ�
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            result = writeET199File(pET199, terminalNumFileID, 0, System.Text.Encoding.Default.GetBytes(this.txtTerminalNo.Text.ToString().Trim()), 8); //д���ն˺�
            if (result != "0")
            {
                this.showError(result);
                return;
            }


            result = createET199File(pET199, tDesFileID, 8, 1); // ����3DES��Կ�ļ�
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            result = writeET199File(pET199, tDesFileID, 0, System.Text.Encoding.Default.GetBytes(desKey), 8); // д����Կ�ļ�
            if (result != "0")
            {
                this.showError(result);
                return;
            }

            
            result = createET199File(pET199, merchantNumReaderFileID, merchantNumReaderFileLength, 0); // �����̻��Ŷ�ȡ����
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            byte[] tmp_buffer = new byte[merchantNumReaderFileLength];
            new System.IO.FileStream(merchantNumReaderFile, System.IO.FileMode.Open, System.IO.FileAccess.Read).Read(tmp_buffer, 0, (int)merchantNumReaderFileLength);
            result = writeET199File(pET199, merchantNumReaderFileID, 0, tmp_buffer, merchantNumReaderFileLength); //д���̻��Ŷ�ȡ����
            if (result != "0")
            {
                this.showError(result);
                return;
            }


            result = createET199File(pET199, terminalNumReaderFileID, terminalNumReaderFileLength, 0); // �����ն˺Ŷ�ȡ����
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            tmp_buffer = new byte[terminalNumReaderFileLength];
            new System.IO.FileStream(terminalNumReaderFile, System.IO.FileMode.Open, System.IO.FileAccess.Read).Read(tmp_buffer, 0, (int)terminalNumReaderFileLength);
            result = writeET199File(pET199, terminalNumReaderFileID, 0, tmp_buffer, terminalNumReaderFileLength); //д���ն˺Ŷ�ȡ����
            if (result != "0")
            {
                this.showError(result);
                return;
            }

            result = createET199File(pET199, tDESReaderFileID, tDESReaderFileLength, 0); // ������Կ��ȡ����
            if (result != "0")
            {
                this.showError(result);
                return;
            }
            tmp_buffer = new byte[tDESReaderFileLength];
            new System.IO.FileStream(tDESReaderFile, System.IO.FileMode.Open, System.IO.FileAccess.Read).Read(tmp_buffer, 0, (int)tDESReaderFileLength);
            result = writeET199File(pET199, tDESReaderFileID, 0, tmp_buffer, tDESReaderFileLength); //д����Կ��ȡ����
            if (result != "0")
            {
                this.showError(result);
                return;
            }            

            // �ر��豸
            dwRet = ETClose(pET199);
            if (dwRet != 0)
            {
                this.showError(dwRet);
                return;
            }


            this.showState("д�����");
            MessageBox.Show("д�����");
            this.showState("����");
            this.EnableControls();
        }
       
        private void Form1_Load(object sender, EventArgs e)
        {
            this.UpdateLengthInfo();
        }

        /// <summary>
        /// ����״̬���ı�������Ϣ
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
            this.openFileDialog1.Filter = "ET199����(*.bin)|*.bin";
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
            this.openFileDialog1.Filter = "ET199����(*.bin)|*.bin";
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
            this.openFileDialog1.Filter = "ET199����(*.bin)|*.bin";
            this.openFileDialog1.Multiselect = false;
            if (this.openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                this.txttDESReaderPgm.Text = this.openFileDialog1.FileName;
            }
        }
        
        /// <summary>
        /// ��������ַ���
        /// </summary>
        /// <param name="length">Ŀ���ַ����ĳ���</param>
        /// <param name="useNum">�Ƿ�������֣�1=������Ĭ��Ϊ����</param>
        /// <param name="useLow">�Ƿ����Сд��ĸ��1=������Ĭ��Ϊ����</param>
        /// <param name="useUpp">�Ƿ������д��ĸ��1=������Ĭ��Ϊ����</param>
        /// <param name="useSpe">�Ƿ���������ַ���1=������Ĭ��Ϊ������</param>
        /// <param name="custom">Ҫ�������Զ����ַ���ֱ������Ҫ�������ַ��б�</param>
        /// <returns>ָ�����ȵ�����ַ���</returns>
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