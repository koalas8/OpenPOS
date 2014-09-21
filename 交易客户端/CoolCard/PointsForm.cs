using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace CoolCard
{
    public partial class PointsForm : Form
    {
        public PointsForm()
        {
            InitializeComponent();
            this.KeyPreview = true;
            this.ControlBox = false;
        }

        private void PointsForm_KeyDown(object sender, KeyEventArgs e)
        {
            //����Ƿ�ȡ���˽���
            Config cfg = new Config();
            if (e.KeyValue.ToString() == cfg.getCancelKeyValue())
            {
                this.Close();
            }
            else if (e.KeyCode == Keys.NumPad1) //��������
            {
                do_points_payment();
            }
            else if (e.KeyCode == Keys.NumPad2) //���ֳ�ֵ(�����ۼ�)
            {
                do_points_deposit();
            }
        }

        /*
         *�������ѽ��� 
         */
        private void do_points_payment()
        {
            MainForm.trans.init();
            MainForm.trans.Action = "points_payment";
            InputForm iForm = new InputForm();
            iForm.InputType = "card"; //ˢ��
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            iForm.InputType = "point"; //�������ѻ���
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            iForm.InputType = "password"; // �ֿ�����������
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            //String dataPackage = MainForm.trans.Build_Trans_String();

            MainForm.trans.Batch_No = Utils.getBatchNum();
            MainForm.trans.Trace_No = Utils.getTraceNum();

            MainForm.send_trans(MainForm.trans);
        }


        /*
         * ���ֳ�ֵ(�����ۼ�)����
         */
        private void do_points_deposit()
        {
            MainForm.trans.init();
            MainForm.trans.Action = "points_deposit";
            InputForm iForm = new InputForm();
            iForm.InputType = "card"; //ˢ��
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            iForm.InputType = "point"; //�����ֵ����
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            //iForm.InputType = "master"; //������������
            //iForm.ShowDialog();
            //if (MainForm.trans.Is_Canceled) return;

            iForm.InputType = "password"; //�ֿ�����������
            iForm.ShowDialog();
            if(MainForm.trans.Is_Canceled) return;

            //String dataPackage = MainForm.trans.Build_Trans_String();

            MainForm.trans.Batch_No = Utils.getBatchNum();
            MainForm.trans.Trace_No = Utils.getTraceNum();

            MainForm .send_trans (MainForm.trans);
        }
                
    }
}