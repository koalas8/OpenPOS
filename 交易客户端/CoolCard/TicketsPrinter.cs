using System;
using System.Collections.Generic;
using System.Collections;
using System.Text;
using System.Drawing;
using System.Drawing.Printing;

namespace CoolCard
{
    class TicketsPrinter
    {
        private String printString = "";        
        public String PrintString
        {
            get { return printString; }
            set { printString = value; }
        }

        
        public void printTicket()
        {
            PrintDocument pd = new PrintDocument();
            pd.PrintController = new StandardPrintController();
            pd.PrintPage += new PrintPageEventHandler(pd_PrintPage);
            pd.Print();
        }

        void pd_PrintPage(object sender, PrintPageEventArgs e)
        {            
            Graphics g = e.Graphics;
            g.DrawString(this.printString, new Font("ËÎÌו", 10), Brushes.Black, new PointF(0,0));
        }      
    }
}
