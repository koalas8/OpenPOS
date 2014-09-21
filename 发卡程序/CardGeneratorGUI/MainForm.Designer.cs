namespace CardGeneratorGUI
{
    partial class MainForm
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
            System.Windows.Forms.Label label1;
            System.Windows.Forms.Label label10;
            System.Windows.Forms.Label label9;
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.rtbRemark = new System.Windows.Forms.RichTextBox();
            this.label11 = new System.Windows.Forms.Label();
            this.btnDefault = new System.Windows.Forms.Button();
            this.label4 = new System.Windows.Forms.Label();
            this.labelBatchInfor = new System.Windows.Forms.Label();
            this.btnGenerateCard = new System.Windows.Forms.Button();
            this.chkNoPass = new System.Windows.Forms.CheckBox();
            this.chkRandomPass = new System.Windows.Forms.CheckBox();
            this.txtCardCount = new System.Windows.Forms.TextBox();
            this.label8 = new System.Windows.Forms.Label();
            this.txtValidLife = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.txtPointsRule = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.txtPoints = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.txtAmount = new System.Windows.Forms.TextBox();
            this.labelAmount = new System.Windows.Forms.Label();
            this.txtPassword = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.cmbCreditUnit = new System.Windows.Forms.ComboBox();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.txtUnitBatch = new System.Windows.Forms.TextBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.chkNotGeneratedFile = new System.Windows.Forms.CheckBox();
            this.chkGeneratedFile = new System.Windows.Forms.CheckBox();
            this.cmbBatchNumToGenFile = new System.Windows.Forms.ComboBox();
            this.cmbUnitToGenFile = new System.Windows.Forms.ComboBox();
            this.labelGenInfo = new System.Windows.Forms.Label();
            this.btnQuery = new System.Windows.Forms.Button();
            this.btnGenFile = new System.Windows.Forms.Button();
            this.dgvGenInfor = new System.Windows.Forms.DataGridView();
            this.dgvColCardNum = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dgvColTrack2 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dgvColPassword = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dgvColValidLife = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            label1 = new System.Windows.Forms.Label();
            label10 = new System.Windows.Forms.Label();
            label9 = new System.Windows.Forms.Label();
            this.tabControl1.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.tabPage2.SuspendLayout();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dgvGenInfor)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new System.Drawing.Point(18, 21);
            label1.Name = "label1";
            label1.Size = new System.Drawing.Size(53, 12);
            label1.TabIndex = 20;
            label1.Text = "发卡集团";
            // 
            // label10
            // 
            label10.AutoSize = true;
            label10.Location = new System.Drawing.Point(17, 49);
            label10.Name = "label10";
            label10.Size = new System.Drawing.Size(41, 12);
            label10.TabIndex = 30;
            label10.Text = "批次号";
            // 
            // label9
            // 
            label9.AutoSize = true;
            label9.Location = new System.Drawing.Point(17, 23);
            label9.Name = "label9";
            label9.Size = new System.Drawing.Size(53, 12);
            label9.TabIndex = 28;
            label9.Text = "发卡集团";
            // 
            // tabControl1
            // 
            this.tabControl1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.tabControl1.Controls.Add(this.tabPage1);
            this.tabControl1.Controls.Add(this.tabPage2);
            this.tabControl1.Location = new System.Drawing.Point(12, 12);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(673, 443);
            this.tabControl1.TabIndex = 0;
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.rtbRemark);
            this.tabPage1.Controls.Add(this.label11);
            this.tabPage1.Controls.Add(this.btnDefault);
            this.tabPage1.Controls.Add(this.label4);
            this.tabPage1.Controls.Add(this.labelBatchInfor);
            this.tabPage1.Controls.Add(this.btnGenerateCard);
            this.tabPage1.Controls.Add(this.chkNoPass);
            this.tabPage1.Controls.Add(this.chkRandomPass);
            this.tabPage1.Controls.Add(this.txtCardCount);
            this.tabPage1.Controls.Add(this.label8);
            this.tabPage1.Controls.Add(this.txtValidLife);
            this.tabPage1.Controls.Add(this.label7);
            this.tabPage1.Controls.Add(this.txtPointsRule);
            this.tabPage1.Controls.Add(this.label6);
            this.tabPage1.Controls.Add(this.txtPoints);
            this.tabPage1.Controls.Add(this.label5);
            this.tabPage1.Controls.Add(this.txtAmount);
            this.tabPage1.Controls.Add(this.labelAmount);
            this.tabPage1.Controls.Add(this.txtPassword);
            this.tabPage1.Controls.Add(this.label3);
            this.tabPage1.Controls.Add(this.cmbCreditUnit);
            this.tabPage1.Controls.Add(label1);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(665, 417);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "发卡";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // rtbRemark
            // 
            this.rtbRemark.Location = new System.Drawing.Point(96, 216);
            this.rtbRemark.Name = "rtbRemark";
            this.rtbRemark.Size = new System.Drawing.Size(545, 72);
            this.rtbRemark.TabIndex = 44;
            this.rtbRemark.Text = "";
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(18, 219);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(29, 12);
            this.label11.TabIndex = 43;
            this.label11.Text = "备注";
            // 
            // btnDefault
            // 
            this.btnDefault.Location = new System.Drawing.Point(20, 379);
            this.btnDefault.Name = "btnDefault";
            this.btnDefault.Size = new System.Drawing.Size(82, 23);
            this.btnDefault.TabIndex = 42;
            this.btnDefault.Text = "选择默认值";
            this.btnDefault.UseVisualStyleBackColor = true;
            this.btnDefault.Click += new System.EventHandler(this.btnDefault_Click);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(18, 331);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(347, 12);
            this.label4.TabIndex = 41;
            this.label4.Text = "卡号格式：3位卡BIN + 4位集团号 +  1位密码标志 + 8位卡序号";
            // 
            // labelBatchInfor
            // 
            this.labelBatchInfor.AutoSize = true;
            this.labelBatchInfor.Location = new System.Drawing.Point(94, 42);
            this.labelBatchInfor.Name = "labelBatchInfor";
            this.labelBatchInfor.Size = new System.Drawing.Size(149, 12);
            this.labelBatchInfor.TabIndex = 40;
            this.labelBatchInfor.Text = "所选集团发卡批次号：未知";
            // 
            // btnGenerateCard
            // 
            this.btnGenerateCard.Location = new System.Drawing.Point(544, 379);
            this.btnGenerateCard.Name = "btnGenerateCard";
            this.btnGenerateCard.Size = new System.Drawing.Size(75, 23);
            this.btnGenerateCard.TabIndex = 38;
            this.btnGenerateCard.Text = "开始发卡";
            this.btnGenerateCard.UseVisualStyleBackColor = true;
            this.btnGenerateCard.Click += new System.EventHandler(this.btnGenerateCard_Click);
            // 
            // chkNoPass
            // 
            this.chkNoPass.AutoSize = true;
            this.chkNoPass.Location = new System.Drawing.Point(555, 101);
            this.chkNoPass.Name = "chkNoPass";
            this.chkNoPass.Size = new System.Drawing.Size(84, 16);
            this.chkNoPass.TabIndex = 37;
            this.chkNoPass.Text = "无初始密码";
            this.chkNoPass.UseVisualStyleBackColor = true;
            this.chkNoPass.CheckedChanged += new System.EventHandler(this.chkNoPass_CheckedChanged);
            // 
            // chkRandomPass
            // 
            this.chkRandomPass.AutoSize = true;
            this.chkRandomPass.Location = new System.Drawing.Point(453, 101);
            this.chkRandomPass.Name = "chkRandomPass";
            this.chkRandomPass.Size = new System.Drawing.Size(96, 16);
            this.chkRandomPass.TabIndex = 36;
            this.chkRandomPass.Text = "随机生成密码";
            this.chkRandomPass.UseVisualStyleBackColor = true;
            this.chkRandomPass.CheckedChanged += new System.EventHandler(this.chkRandomPass_CheckedChanged);
            // 
            // txtCardCount
            // 
            this.txtCardCount.Location = new System.Drawing.Point(96, 178);
            this.txtCardCount.Name = "txtCardCount";
            this.txtCardCount.Size = new System.Drawing.Size(183, 21);
            this.txtCardCount.TabIndex = 35;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(18, 181);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(53, 12);
            this.label8.TabIndex = 34;
            this.label8.Text = "制卡数量";
            // 
            // txtValidLife
            // 
            this.txtValidLife.Location = new System.Drawing.Point(453, 140);
            this.txtValidLife.Name = "txtValidLife";
            this.txtValidLife.Size = new System.Drawing.Size(183, 21);
            this.txtValidLife.TabIndex = 33;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(375, 143);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(65, 12);
            this.label7.TabIndex = 32;
            this.label7.Text = "有效期(月)";
            // 
            // txtPointsRule
            // 
            this.txtPointsRule.Location = new System.Drawing.Point(453, 178);
            this.txtPointsRule.Name = "txtPointsRule";
            this.txtPointsRule.Size = new System.Drawing.Size(183, 21);
            this.txtPointsRule.TabIndex = 31;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(375, 181);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(53, 12);
            this.label6.TabIndex = 30;
            this.label6.Text = "积分规则";
            // 
            // txtPoints
            // 
            this.txtPoints.Location = new System.Drawing.Point(96, 140);
            this.txtPoints.Name = "txtPoints";
            this.txtPoints.Size = new System.Drawing.Size(183, 21);
            this.txtPoints.TabIndex = 29;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(18, 143);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(53, 12);
            this.label5.TabIndex = 28;
            this.label5.Text = "初始积分";
            // 
            // txtAmount
            // 
            this.txtAmount.Location = new System.Drawing.Point(96, 74);
            this.txtAmount.Name = "txtAmount";
            this.txtAmount.Size = new System.Drawing.Size(183, 21);
            this.txtAmount.TabIndex = 27;
            // 
            // labelAmount
            // 
            this.labelAmount.AutoSize = true;
            this.labelAmount.Location = new System.Drawing.Point(18, 77);
            this.labelAmount.Name = "labelAmount";
            this.labelAmount.Size = new System.Drawing.Size(53, 12);
            this.labelAmount.TabIndex = 26;
            this.labelAmount.Text = "初始金额";
            // 
            // txtPassword
            // 
            this.txtPassword.Location = new System.Drawing.Point(453, 74);
            this.txtPassword.Name = "txtPassword";
            this.txtPassword.Size = new System.Drawing.Size(183, 21);
            this.txtPassword.TabIndex = 25;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(375, 77);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(53, 12);
            this.label3.TabIndex = 24;
            this.label3.Text = "初始密码";
            // 
            // cmbCreditUnit
            // 
            this.cmbCreditUnit.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cmbCreditUnit.FormattingEnabled = true;
            this.cmbCreditUnit.Location = new System.Drawing.Point(96, 18);
            this.cmbCreditUnit.Name = "cmbCreditUnit";
            this.cmbCreditUnit.Size = new System.Drawing.Size(540, 20);
            this.cmbCreditUnit.TabIndex = 21;
            this.cmbCreditUnit.SelectedIndexChanged += new System.EventHandler(this.cmbCreditUnit_SelectedIndexChanged);
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.txtUnitBatch);
            this.tabPage2.Controls.Add(this.groupBox1);
            this.tabPage2.Controls.Add(this.labelGenInfo);
            this.tabPage2.Controls.Add(this.btnQuery);
            this.tabPage2.Controls.Add(this.btnGenFile);
            this.tabPage2.Controls.Add(this.dgvGenInfor);
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(665, 417);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "生成制卡文件";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // txtUnitBatch
            // 
            this.txtUnitBatch.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.txtUnitBatch.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.txtUnitBatch.Location = new System.Drawing.Point(355, 393);
            this.txtUnitBatch.Name = "txtUnitBatch";
            this.txtUnitBatch.ReadOnly = true;
            this.txtUnitBatch.Size = new System.Drawing.Size(200, 21);
            this.txtUnitBatch.TabIndex = 33;
            // 
            // groupBox1
            // 
            this.groupBox1.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.groupBox1.Controls.Add(this.chkNotGeneratedFile);
            this.groupBox1.Controls.Add(this.chkGeneratedFile);
            this.groupBox1.Controls.Add(this.cmbBatchNumToGenFile);
            this.groupBox1.Controls.Add(label10);
            this.groupBox1.Controls.Add(this.cmbUnitToGenFile);
            this.groupBox1.Controls.Add(label9);
            this.groupBox1.Location = new System.Drawing.Point(8, 3);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(570, 81);
            this.groupBox1.TabIndex = 32;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "选择集团和批次号";
            // 
            // chkNotGeneratedFile
            // 
            this.chkNotGeneratedFile.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.chkNotGeneratedFile.AutoSize = true;
            this.chkNotGeneratedFile.Checked = true;
            this.chkNotGeneratedFile.CheckState = System.Windows.Forms.CheckState.Checked;
            this.chkNotGeneratedFile.Location = new System.Drawing.Point(379, 48);
            this.chkNotGeneratedFile.Name = "chkNotGeneratedFile";
            this.chkNotGeneratedFile.Size = new System.Drawing.Size(168, 16);
            this.chkNotGeneratedFile.TabIndex = 33;
            this.chkNotGeneratedFile.Text = "显示未生成制卡文件的批次";
            this.chkNotGeneratedFile.UseVisualStyleBackColor = true;
            this.chkNotGeneratedFile.CheckedChanged += new System.EventHandler(this.chkNotGeneratedFile_CheckedChanged);
            // 
            // chkGeneratedFile
            // 
            this.chkGeneratedFile.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.chkGeneratedFile.AutoSize = true;
            this.chkGeneratedFile.Location = new System.Drawing.Point(205, 48);
            this.chkGeneratedFile.Name = "chkGeneratedFile";
            this.chkGeneratedFile.Size = new System.Drawing.Size(168, 16);
            this.chkGeneratedFile.TabIndex = 32;
            this.chkGeneratedFile.Text = "显示已生成制卡文件的批次";
            this.chkGeneratedFile.UseVisualStyleBackColor = true;
            this.chkGeneratedFile.Visible = false;
            this.chkGeneratedFile.CheckedChanged += new System.EventHandler(this.chkGeneratedFile_CheckedChanged);
            // 
            // cmbBatchNumToGenFile
            // 
            this.cmbBatchNumToGenFile.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.cmbBatchNumToGenFile.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cmbBatchNumToGenFile.FormattingEnabled = true;
            this.cmbBatchNumToGenFile.Location = new System.Drawing.Point(95, 46);
            this.cmbBatchNumToGenFile.Name = "cmbBatchNumToGenFile";
            this.cmbBatchNumToGenFile.Size = new System.Drawing.Size(104, 20);
            this.cmbBatchNumToGenFile.TabIndex = 31;
            // 
            // cmbUnitToGenFile
            // 
            this.cmbUnitToGenFile.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.cmbUnitToGenFile.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cmbUnitToGenFile.FormattingEnabled = true;
            this.cmbUnitToGenFile.Location = new System.Drawing.Point(95, 20);
            this.cmbUnitToGenFile.Name = "cmbUnitToGenFile";
            this.cmbUnitToGenFile.Size = new System.Drawing.Size(452, 20);
            this.cmbUnitToGenFile.TabIndex = 29;
            this.cmbUnitToGenFile.SelectedIndexChanged += new System.EventHandler(this.cmbUnitToGenFile_SelectedIndexChanged);
            // 
            // labelGenInfo
            // 
            this.labelGenInfo.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelGenInfo.AutoSize = true;
            this.labelGenInfo.Location = new System.Drawing.Point(6, 396);
            this.labelGenInfo.Name = "labelGenInfo";
            this.labelGenInfo.Size = new System.Drawing.Size(0, 12);
            this.labelGenInfo.TabIndex = 31;
            // 
            // btnQuery
            // 
            this.btnQuery.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.btnQuery.Location = new System.Drawing.Point(584, 10);
            this.btnQuery.Name = "btnQuery";
            this.btnQuery.Size = new System.Drawing.Size(75, 74);
            this.btnQuery.TabIndex = 30;
            this.btnQuery.Text = "查询";
            this.btnQuery.UseVisualStyleBackColor = true;
            this.btnQuery.Click += new System.EventHandler(this.btnQuery_Click);
            // 
            // btnGenFile
            // 
            this.btnGenFile.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.btnGenFile.Location = new System.Drawing.Point(584, 391);
            this.btnGenFile.Name = "btnGenFile";
            this.btnGenFile.Size = new System.Drawing.Size(75, 23);
            this.btnGenFile.TabIndex = 29;
            this.btnGenFile.Text = "生成";
            this.btnGenFile.UseVisualStyleBackColor = true;
            this.btnGenFile.Click += new System.EventHandler(this.btnGenFile_Click);
            // 
            // dgvGenInfor
            // 
            this.dgvGenInfor.AllowUserToAddRows = false;
            this.dgvGenInfor.AllowUserToDeleteRows = false;
            this.dgvGenInfor.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.dgvGenInfor.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgvGenInfor.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.dgvColCardNum,
            this.dgvColTrack2,
            this.dgvColPassword,
            this.dgvColValidLife});
            this.dgvGenInfor.Location = new System.Drawing.Point(6, 90);
            this.dgvGenInfor.Name = "dgvGenInfor";
            this.dgvGenInfor.RowTemplate.Height = 20;
            this.dgvGenInfor.RowTemplate.ReadOnly = true;
            this.dgvGenInfor.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.dgvGenInfor.Size = new System.Drawing.Size(653, 298);
            this.dgvGenInfor.TabIndex = 28;
            this.dgvGenInfor.RowPostPaint += new System.Windows.Forms.DataGridViewRowPostPaintEventHandler(this.dgvGenInfor_RowPostPaint);
            // 
            // dgvColCardNum
            // 
            this.dgvColCardNum.HeaderText = "卡号";
            this.dgvColCardNum.MaxInputLength = 19;
            this.dgvColCardNum.Name = "dgvColCardNum";
            this.dgvColCardNum.ReadOnly = true;
            this.dgvColCardNum.Width = 140;
            // 
            // dgvColTrack2
            // 
            this.dgvColTrack2.HeaderText = "二磁道数据";
            this.dgvColTrack2.MaxInputLength = 34;
            this.dgvColTrack2.Name = "dgvColTrack2";
            this.dgvColTrack2.ReadOnly = true;
            this.dgvColTrack2.Width = 250;
            // 
            // dgvColPassword
            // 
            this.dgvColPassword.HeaderText = "卡密码";
            this.dgvColPassword.MaxInputLength = 6;
            this.dgvColPassword.Name = "dgvColPassword";
            this.dgvColPassword.ReadOnly = true;
            this.dgvColPassword.Width = 90;
            // 
            // dgvColValidLife
            // 
            this.dgvColValidLife.HeaderText = "有效期(月)";
            this.dgvColValidLife.MaxInputLength = 3;
            this.dgvColValidLife.Name = "dgvColValidLife";
            this.dgvColValidLife.ReadOnly = true;
            this.dgvColValidLife.Width = 90;
            // 
            // saveFileDialog1
            // 
            this.saveFileDialog1.DefaultExt = "txt";
            this.saveFileDialog1.Filter = "文本文件|*.txt";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(697, 468);
            this.Controls.Add(this.tabControl1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MaximumSize = new System.Drawing.Size(713, 506);
            this.MinimizeBox = false;
            this.MinimumSize = new System.Drawing.Size(713, 506);
            this.Name = "MainForm";
            this.Text = "CoolCard生成管理软件";
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.tabControl1.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            this.tabPage1.PerformLayout();
            this.tabPage2.ResumeLayout(false);
            this.tabPage2.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dgvGenInfor)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.Button btnGenerateCard;
        private System.Windows.Forms.CheckBox chkNoPass;
        private System.Windows.Forms.CheckBox chkRandomPass;
        private System.Windows.Forms.TextBox txtCardCount;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.TextBox txtValidLife;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox txtPointsRule;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox txtPoints;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox txtAmount;
        private System.Windows.Forms.Label labelAmount;
        private System.Windows.Forms.TextBox txtPassword;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.ComboBox cmbCreditUnit;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.Label labelBatchInfor;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button btnGenFile;
        private System.Windows.Forms.DataGridView dgvGenInfor;
        private System.Windows.Forms.Button btnQuery;
        private System.Windows.Forms.Label labelGenInfo;
        private System.Windows.Forms.DataGridViewTextBoxColumn dgvColCardNum;
        private System.Windows.Forms.DataGridViewTextBoxColumn dgvColTrack2;
        private System.Windows.Forms.DataGridViewTextBoxColumn dgvColPassword;
        private System.Windows.Forms.DataGridViewTextBoxColumn dgvColValidLife;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.CheckBox chkNotGeneratedFile;
        private System.Windows.Forms.CheckBox chkGeneratedFile;
        private System.Windows.Forms.ComboBox cmbBatchNumToGenFile;
        private System.Windows.Forms.ComboBox cmbUnitToGenFile;
        private System.Windows.Forms.TextBox txtUnitBatch;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.Button btnDefault;
        private System.Windows.Forms.RichTextBox rtbRemark;
        private System.Windows.Forms.Label label11;

    }
}

