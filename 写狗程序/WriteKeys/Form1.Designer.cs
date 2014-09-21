namespace WriteKeys
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.label1 = new System.Windows.Forms.Label();
            this.txtMerchantNo = new System.Windows.Forms.TextBox();
            this.txtTerminalNo = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.button1 = new System.Windows.Forms.Button();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.toolStripStatusLabel1 = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripStatusLabel2 = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripStatusLabel3 = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripStatusLabel4 = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripStatusLabel_Merchant_length = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripStatusLabel5 = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripStatusLabel_Terminal_length = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripStatusLabel_3DES_Length = new System.Windows.Forms.ToolStripStatusLabel();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.btnBrowseMerchNumReader = new System.Windows.Forms.Button();
            this.txtMerchantNumReaderPgm = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.btnBrowseTermNumReader = new System.Windows.Forms.Button();
            this.txtTerminalNumReaderPgm = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.button2 = new System.Windows.Forms.Button();
            this.txttDESReaderPgm = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.statusStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(26, 110);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(41, 12);
            this.label1.TabIndex = 0;
            this.label1.Text = "商户号";
            // 
            // txtMerchantNo
            // 
            this.txtMerchantNo.Location = new System.Drawing.Point(127, 107);
            this.txtMerchantNo.MaxLength = 15;
            this.txtMerchantNo.Name = "txtMerchantNo";
            this.txtMerchantNo.Size = new System.Drawing.Size(275, 21);
            this.txtMerchantNo.TabIndex = 1;
            this.txtMerchantNo.TextChanged += new System.EventHandler(this.txtMerchantNo_TextChanged);
            // 
            // txtTerminalNo
            // 
            this.txtTerminalNo.Location = new System.Drawing.Point(127, 134);
            this.txtTerminalNo.MaxLength = 8;
            this.txtTerminalNo.Name = "txtTerminalNo";
            this.txtTerminalNo.Size = new System.Drawing.Size(275, 21);
            this.txtTerminalNo.TabIndex = 3;
            this.txtTerminalNo.TextChanged += new System.EventHandler(this.txtTerminalNo_TextChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(26, 137);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(41, 12);
            this.label2.TabIndex = 2;
            this.label2.Text = "终端号";
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(408, 110);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(153, 48);
            this.button1.TabIndex = 6;
            this.button1.Text = "开始写入";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // statusStrip1
            // 
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripStatusLabel1,
            this.toolStripStatusLabel2,
            this.toolStripStatusLabel3,
            this.toolStripStatusLabel4,
            this.toolStripStatusLabel_Merchant_length,
            this.toolStripStatusLabel5,
            this.toolStripStatusLabel_Terminal_length,
            this.toolStripStatusLabel_3DES_Length});
            this.statusStrip1.Location = new System.Drawing.Point(0, 171);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(592, 22);
            this.statusStrip1.TabIndex = 8;
            this.statusStrip1.Text = "statusStrip1";
            // 
            // toolStripStatusLabel1
            // 
            this.toolStripStatusLabel1.Name = "toolStripStatusLabel1";
            this.toolStripStatusLabel1.Size = new System.Drawing.Size(35, 17);
            this.toolStripStatusLabel1.Text = "状态:";
            // 
            // toolStripStatusLabel2
            // 
            this.toolStripStatusLabel2.Name = "toolStripStatusLabel2";
            this.toolStripStatusLabel2.Size = new System.Drawing.Size(29, 17);
            this.toolStripStatusLabel2.Text = "就绪";
            // 
            // toolStripStatusLabel3
            // 
            this.toolStripStatusLabel3.Name = "toolStripStatusLabel3";
            this.toolStripStatusLabel3.Size = new System.Drawing.Size(119, 17);
            this.toolStripStatusLabel3.Text = "                   ";
            // 
            // toolStripStatusLabel4
            // 
            this.toolStripStatusLabel4.Name = "toolStripStatusLabel4";
            this.toolStripStatusLabel4.Size = new System.Drawing.Size(71, 17);
            this.toolStripStatusLabel4.Text = "商户号长度:";
            // 
            // toolStripStatusLabel_Merchant_length
            // 
            this.toolStripStatusLabel_Merchant_length.Name = "toolStripStatusLabel_Merchant_length";
            this.toolStripStatusLabel_Merchant_length.Size = new System.Drawing.Size(17, 17);
            this.toolStripStatusLabel_Merchant_length.Text = "  ";
            // 
            // toolStripStatusLabel5
            // 
            this.toolStripStatusLabel5.Name = "toolStripStatusLabel5";
            this.toolStripStatusLabel5.Size = new System.Drawing.Size(71, 17);
            this.toolStripStatusLabel5.Text = "终端号长度:";
            // 
            // toolStripStatusLabel_Terminal_length
            // 
            this.toolStripStatusLabel_Terminal_length.Name = "toolStripStatusLabel_Terminal_length";
            this.toolStripStatusLabel_Terminal_length.Size = new System.Drawing.Size(0, 17);
            // 
            // toolStripStatusLabel_3DES_Length
            // 
            this.toolStripStatusLabel_3DES_Length.Name = "toolStripStatusLabel_3DES_Length";
            this.toolStripStatusLabel_3DES_Length.Size = new System.Drawing.Size(0, 17);
            // 
            // btnBrowseMerchNumReader
            // 
            this.btnBrowseMerchNumReader.Location = new System.Drawing.Point(485, 21);
            this.btnBrowseMerchNumReader.Name = "btnBrowseMerchNumReader";
            this.btnBrowseMerchNumReader.Size = new System.Drawing.Size(76, 24);
            this.btnBrowseMerchNumReader.TabIndex = 11;
            this.btnBrowseMerchNumReader.Text = "浏览";
            this.btnBrowseMerchNumReader.UseVisualStyleBackColor = true;
            this.btnBrowseMerchNumReader.Click += new System.EventHandler(this.btnBrowseMerchNumReader_Click);
            // 
            // txtMerchantNumReaderPgm
            // 
            this.txtMerchantNumReaderPgm.Location = new System.Drawing.Point(127, 21);
            this.txtMerchantNumReaderPgm.Name = "txtMerchantNumReaderPgm";
            this.txtMerchantNumReaderPgm.ReadOnly = true;
            this.txtMerchantNumReaderPgm.Size = new System.Drawing.Size(352, 21);
            this.txtMerchantNumReaderPgm.TabIndex = 10;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(26, 24);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(89, 12);
            this.label4.TabIndex = 9;
            this.label4.Text = "商户号读取程序";
            // 
            // btnBrowseTermNumReader
            // 
            this.btnBrowseTermNumReader.Location = new System.Drawing.Point(485, 48);
            this.btnBrowseTermNumReader.Name = "btnBrowseTermNumReader";
            this.btnBrowseTermNumReader.Size = new System.Drawing.Size(76, 24);
            this.btnBrowseTermNumReader.TabIndex = 14;
            this.btnBrowseTermNumReader.Text = "浏览";
            this.btnBrowseTermNumReader.UseVisualStyleBackColor = true;
            this.btnBrowseTermNumReader.Click += new System.EventHandler(this.btnBrowseTermNumReader_Click);
            // 
            // txtTerminalNumReaderPgm
            // 
            this.txtTerminalNumReaderPgm.Location = new System.Drawing.Point(127, 48);
            this.txtTerminalNumReaderPgm.Name = "txtTerminalNumReaderPgm";
            this.txtTerminalNumReaderPgm.ReadOnly = true;
            this.txtTerminalNumReaderPgm.Size = new System.Drawing.Size(352, 21);
            this.txtTerminalNumReaderPgm.TabIndex = 13;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(26, 51);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(89, 12);
            this.label5.TabIndex = 12;
            this.label5.Text = "终端号读取程序";
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(485, 75);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(76, 24);
            this.button2.TabIndex = 17;
            this.button2.Text = "浏览";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // txttDESReaderPgm
            // 
            this.txttDESReaderPgm.Location = new System.Drawing.Point(127, 75);
            this.txttDESReaderPgm.Name = "txttDESReaderPgm";
            this.txttDESReaderPgm.ReadOnly = true;
            this.txttDESReaderPgm.Size = new System.Drawing.Size(352, 21);
            this.txttDESReaderPgm.TabIndex = 16;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(26, 78);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(77, 12);
            this.label3.TabIndex = 15;
            this.label3.Text = "密钥读取程序";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(592, 193);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.txttDESReaderPgm);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.btnBrowseTermNumReader);
            this.Controls.Add(this.txtTerminalNumReaderPgm);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.btnBrowseMerchNumReader);
            this.Controls.Add(this.txtMerchantNumReaderPgm);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.txtTerminalNo);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.txtMerchantNo);
            this.Controls.Add(this.label1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MaximumSize = new System.Drawing.Size(600, 220);
            this.MinimizeBox = false;
            this.MinimumSize = new System.Drawing.Size(600, 220);
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "ET199密钥及参数写入工具";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox txtMerchantNo;
        private System.Windows.Forms.TextBox txtTerminalNo;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel1;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel2;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel3;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel4;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel_Merchant_length;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel5;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel_Terminal_length;
        private System.Windows.Forms.Button btnBrowseMerchNumReader;
        private System.Windows.Forms.TextBox txtMerchantNumReaderPgm;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button btnBrowseTermNumReader;
        private System.Windows.Forms.TextBox txtTerminalNumReaderPgm;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel_3DES_Length;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.TextBox txttDESReaderPgm;
        private System.Windows.Forms.Label label3;
    }
}

