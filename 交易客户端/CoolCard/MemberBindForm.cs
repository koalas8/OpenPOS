using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace CoolCard
{
    public partial class MemberBindForm : Form
    {
        public MemberBindForm()
        {
            InitializeComponent();
        }

        private void btnAddMember_Click(object sender, EventArgs e)
        {
            if (this.txtMemberName.Text.Trim() == "")
            {
                MessageBox.Show("会员名称不能为空!");
                return;
            }

            if (this.txtCellNumber.Text.Trim() == "")
            {
                MessageBox.Show("电话号码不能为空!");
                return;
            }

            if (this.txtCardNumber.Text.Trim() == "")
            {
                MessageBox.Show("卡号不能为空!");
                return;
            }

            Member member = new Member();
            member.Action = "bind_member";
            member.Member_Card_Number = this.txtCardNumber.Text.Trim();
            member.Member_Cell_Number = this.txtCellNumber.Text.Trim();
            member.Member_Name = this.txtMemberName.Text.Trim();           
            member.Member_Id_Number = this.txtIdNumber.Text.Trim();
            member.Member_Remark = this.txtRemark.Text.Trim();
            member.Member_Sex = this.comboBoxSex.Text.Trim();

            string trans_string = member.Build_String();

            MySocket ms = new MySocket();
            string rst = ms.Send(trans_string);

            MessageBox.Show(CoolCard.Config .GetConfig ("ERRORCODE", rst, "未找到消息配置"));
            
        }

        private void MemberBindForm_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Escape)
            {
                this.Close();
            }
        }

        private void MemberBindForm_Load(object sender, EventArgs e)
        {
            this.txtMemberName.Focus();
        }

        private void txtCardNumber_TextChanged(object sender, EventArgs e)
        {
            if (this.txtCardNumber.Text.Trim().Length >= 19)
            {
                this.txtCardNumber.Text = this.txtCardNumber.Text.Substring(0, 19);
            }
        }
    }
}