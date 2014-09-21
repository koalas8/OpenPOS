using System;
using System.Collections;
using System.Data;
using System.Drawing;
using System.Windows.Forms;
using System.IO;

namespace CardGeneratorGUI
{
    public partial class MainForm : Form
    {
        public static Boolean LoginFlag = false;
        public static Boolean CancelLoginFlag = false;

        public MainForm()
        {
            InitializeComponent();
        }

        /// <summary>
        /// 用户登录
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void MainForm_Load(object sender, EventArgs e)
        {
            //   用户登录窗体
            while (LoginFlag == false)
            {                    
                var lForm = new LoginForm();
                lForm.ShowDialog();
                if (CancelLoginFlag != true) continue;
                Close();
                break;
            } // 


            // 显示主窗体时要在集团下拉框中准备好数据
            var unitList = new ArrayList();
            unitList = CardGenerator.Generator.GetAllUnits();
            foreach (String s in unitList)
            {
                cmbCreditUnit.Items.Add(s);
                cmbUnitToGenFile.Items.Add(s);
            } //
        }

        /// <summary>
        /// 选择发卡集团时要显示此集团的发卡批次号
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void cmbCreditUnit_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cmbCreditUnit.Text.Trim() == "")
            {
                labelBatchInfor.Text = "所选集团发卡批次号：未知      所选集团发卡起始号:未知";
            }
            else
            {
                labelBatchInfor.Text = "所选集团发卡批次号：" 
                    + CardGenerator.Generator.GetCurrentBatchNum(cmbCreditUnit.Text.Substring(0,4)).ToString()
                    + "      所选集团发卡起始号:"
                    + CardGenerator.Generator.GetStartCardNum(cmbCreditUnit.Text.Substring(0,4)).ToString();
            }
        }


        /// <summary>
        /// 卡类型（储值卡/储次卡）下拉框变化时，金额标签也要变化
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        //private void cmbCardKind_SelectedIndexChanged(object sender, EventArgs e)
        //{
        //    if (cmbCardKind.Text.Trim() == "" || cmbCardKind.Text.Trim().Substring(0, 1) == "0")
        //    {
        //        labelAmount.Text = "初始金额";
        //    }
        //    else if (cmbCardKind.Text.Trim().Substring(0, 1) == "1")
        //    {
        //        labelAmount.Text = "初始次数";
        //    }
        //}


        /// <summary>
        /// 随机密码选择框变化时要设置与其相关的控件的变化
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void chkRandomPass_CheckedChanged(object sender, EventArgs e)
        {
            if (chkRandomPass.Checked)
            {
                chkNoPass.Checked = false;
                txtPassword.ReadOnly = true;
                txtPassword.Text = "";
            }
            else
            {
                txtPassword.ReadOnly = false;
            }
        }

        /// <summary>
        /// 无密码选择框变化时要设置与其相关的控件的变化
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void chkNoPass_CheckedChanged(object sender, EventArgs e)
        {
            if (chkNoPass.Checked)
            {
                chkRandomPass.Checked = false;
                txtPassword.ReadOnly = true;
                txtPassword.Text = "";
            }
            else
            {
                this.txtPassword.ReadOnly = false;
            }
        }

        /// <summary>
        /// 检查表单是否填写完整
        /// </summary>
        /// <returns>是-返回"0";否-返回错误信息,此信息可直接用MessageBox显示出来</returns>
        private String CheckForm()
        {
            if (cmbCreditUnit.Text.Trim() == "")
            {
                return "请选择发卡集团";
            }
            //if (cmbCardKind.Text.Trim() == "")
            //{
            //    return "请选择所发卡类型";
            //}
            if ((!chkNoPass.Checked) && (!chkRandomPass.Checked))
            {
                if (txtPassword.Text.Trim() == "")
                {
                    return "请设置密码";
                }
                if (txtPassword.Text.Trim().Length != 6)
                {
                    return "初始密码必须为6位";
                }
            }

            if (txtAmount.Text.Trim() == "")
            {
                return "请输入初始金额";
            }
            if (txtValidLife.Text.Trim() == "")
            {
                return "请输入卡有效期";
            }
            if (txtPoints.Text.Trim() == "")
            {
                return "请输入初始积分";
            }
            if (txtPointsRule.Text.Trim() == "")
            {
                return "请输入积分规则";
            }
            if (txtCardCount.Text.Trim() == "" || txtCardCount.Text.Trim() == "0")
            {
                return "请输入制卡数量";
            }

            return "0";
        }


        private void btnGenerateCard_Click(object sender, EventArgs e)
        {
            String checkFormResult = this.CheckForm();
            if (checkFormResult != "0")
            {
                MessageBox.Show(checkFormResult);
                return;
            }

            String unit = cmbCreditUnit.Text.Trim().Substring(0, 4);  // 发卡集团集团号
            //String cardKind = cmbCardKind.Text.Trim().Substring(0, 1);  // 卡类型
            String password = txtPassword.Text.Trim();  // 初始密码
            Boolean passwordFlag = !chkNoPass.Checked;
            //Boolean depositFlag = chkDepositFlag.Checked;
            Boolean randomPassFlag = chkRandomPass.Checked;
            int amount = Convert.ToInt32(txtAmount.Text.Trim());
            int validLife = Convert.ToInt32(txtValidLife.Text.Trim());
            int points = Convert.ToInt32(txtPoints.Text.Trim());
            int pointsRule = Convert.ToInt32(txtPointsRule.Text.Trim());
            int cardCount = Convert.ToInt32(txtCardCount.Text.Trim());
            String remark = rtbRemark.Text.Trim();

            String result = CardGenerator.Generator.GenerateCards(
                "207", 
                unit, 
                "0",
                true,
                passwordFlag, 
                randomPassFlag, 
                password, 
                amount, 
                points, 
                pointsRule, 
                validLife, 
                cardCount, 
                remark);

            MessageBox.Show("发卡成功");

        }


        private void GetGenFileBatchNum()
        {
            if (cmbUnitToGenFile.Text.Trim() == "")
            {
                return;
            }
            String unitNum = cmbUnitToGenFile.Text.Trim().Substring(0, 4);
            ArrayList batchArray = CardGenerator.Generator.GetAllBatchNums(unitNum, chkGeneratedFile.Checked, chkNotGeneratedFile.Checked);
            cmbBatchNumToGenFile.Items.Clear();
            foreach (int batchNum in batchArray)
            {
                cmbBatchNumToGenFile.Items.Add(batchNum);
            }
            dgvGenInfor.Rows.Clear();
        }


        private void btnQuery_Click(object sender, EventArgs e)
        {
            if (cmbUnitToGenFile.Text.Trim() == "")
            {
                MessageBox.Show("请选择集团");
                return;
            }
            if (cmbBatchNumToGenFile.Text.Trim() == "")
            {
                MessageBox.Show("请选择批次号");
                return;
            }

            String unitNum = cmbUnitToGenFile.Text.Trim().Substring(0, 4);
            String batchNum = cmbBatchNumToGenFile.Text.Trim();

            DataTable dt = new DataTable();            
            dt = CardGenerator.Generator.QueryGenFile(unitNum, Convert.ToInt32(batchNum));
            labelGenInfo.Text = String.Format("集团 [{0}]，当前批次 [{1}]，卡 [{2}张]", cmbUnitToGenFile.Text.Trim(), batchNum, dt.Rows.Count.ToString());
            txtUnitBatch.Text = unitNum + "-" + batchNum;
            dgvGenInfor.Rows.Clear();
            foreach (DataRow dr in dt.Rows)
            {
                dgvGenInfor.Rows.Add(new object[] { dr["card_no"], dr["track_2"], dr["password"], dr["valid_life"]});
            }            
        }

        private void dgvGenInfor_RowPostPaint(object sender, DataGridViewRowPostPaintEventArgs e)
        {
            System.Drawing.Rectangle rectangle = new Rectangle(e.RowBounds.Location.X, e.RowBounds.Location.Y, this.dgvGenInfor.RowHeadersWidth - 3, e.RowBounds.Height);
            TextRenderer.DrawText(e.Graphics, (e.RowIndex + 1).ToString(), this.dgvGenInfor.RowHeadersDefaultCellStyle.Font, rectangle, this.dgvGenInfor.RowHeadersDefaultCellStyle.ForeColor, TextFormatFlags.VerticalCenter | TextFormatFlags.Right);

        }

        private void cmbUnitToGenFile_SelectedIndexChanged(object sender, EventArgs e)
        {
            GetGenFileBatchNum();
        }

        private void chkNotGeneratedFile_CheckedChanged(object sender, EventArgs e)
        {
            GetGenFileBatchNum();
        }

        private void chkGeneratedFile_CheckedChanged(object sender, EventArgs e)
        {
            GetGenFileBatchNum();
        }

        private void btnGenFile_Click(object sender, EventArgs e)
        {
            if (this.dgvGenInfor.Rows.Count == 0)
            {
                MessageBox.Show("没有数据，不能生成制卡文件");
                return;
            }
            
            String unitNum = this.txtUnitBatch.Text.Trim().Split('-')[0];
            String batchNum = this.txtUnitBatch.Text.Trim().Split('-')[1];
            String date = DateTime.Now.ToString("yyyy年MM月dd日HH时mm分ss秒");

            saveFileDialog1.FileName = unitNum + "集团_" + batchNum + "批次_" + date;
            if (saveFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {                
                String file = saveFileDialog1.FileName.Trim();
                if (file == "")
                {
                    MessageBox.Show("请选择输出文件");
                    return;
                }
                StreamWriter sw = new StreamWriter(file);
                sw.WriteLine("发卡集团:" + unitNum + "\t批次号:" + batchNum + "\t发卡日期:" + date);                
                sw.WriteLine("文件格式: 卡号|二磁数据|密码|有效期");
                foreach (DataGridViewRow dr in dgvGenInfor.Rows)
                {
                    sw.WriteLine(String.Format("{0}|{1}|{2}|{3}", dr.Cells[0].Value.ToString().Trim(), dr.Cells[1].Value.ToString().Trim(), dr.Cells[2].Value.ToString().Trim(), dr.Cells[3].Value.ToString().Trim()));
                }
                sw.Close();
                
                if(CardGenerator.Generator.CommitGenFile(unitNum, Convert.ToInt32(batchNum)))
                {
                    MessageBox.Show("更新账户成功");
                }
                else
                {
                    MessageBox.Show("更新账户失败");
                }
                MessageBox.Show("生成制卡文件成功");
                dgvGenInfor.Rows.Clear();
                GetGenFileBatchNum();
            }
        }

        private void btnDefault_Click(object sender, EventArgs e)
        {
            //cmbCardKind.SelectedIndex = 0;
            //chkDepositFlag.Checked = true;
            txtPassword.Text = "000000";
            chkNoPass.Checked = false;
            chkRandomPass.Checked = false;
            txtAmount.Text = "0";
            txtPoints.Text = "0";
            txtPointsRule.Text = "0";
            txtValidLife.Text = "12";            
        }
    }
}
