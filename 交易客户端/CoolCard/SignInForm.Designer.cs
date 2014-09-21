namespace CoolCard
{
    partial class SignInForm
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
            this.textBox_operator_no = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.textBox_operator_password = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // textBox_operator_no
            // 
            this.textBox_operator_no.Font = new System.Drawing.Font("宋体", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.textBox_operator_no.Location = new System.Drawing.Point(222, 12);
            this.textBox_operator_no.Name = "textBox_operator_no";
            this.textBox_operator_no.Size = new System.Drawing.Size(194, 47);
            this.textBox_operator_no.TabIndex = 3;
            this.textBox_operator_no.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("宋体", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.label1.Location = new System.Drawing.Point(78, 15);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(138, 35);
            this.label1.TabIndex = 2;
            this.label1.Text = "操作员:";
            // 
            // textBox_operator_password
            // 
            this.textBox_operator_password.Font = new System.Drawing.Font("宋体", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.textBox_operator_password.Location = new System.Drawing.Point(222, 65);
            this.textBox_operator_password.Name = "textBox_operator_password";
            this.textBox_operator_password.PasswordChar = '*';
            this.textBox_operator_password.Size = new System.Drawing.Size(194, 47);
            this.textBox_operator_password.TabIndex = 5;
            this.textBox_operator_password.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("宋体", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.label2.Location = new System.Drawing.Point(8, 68);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(208, 35);
            this.label2.TabIndex = 4;
            this.label2.Text = "操作员密码:";
            // 
            // SignInForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(441, 132);
            this.Controls.Add(this.textBox_operator_password);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.textBox_operator_no);
            this.Controls.Add(this.label1);
            this.KeyPreview = true;
            this.MaximizeBox = false;
            this.MaximumSize = new System.Drawing.Size(449, 159);
            this.MinimizeBox = false;
            this.MinimumSize = new System.Drawing.Size(449, 159);
            this.Name = "SignInForm";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "签到";
            this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.SignInForm_KeyDown);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBox_operator_no;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox textBox_operator_password;
        private System.Windows.Forms.Label label2;
    }
}