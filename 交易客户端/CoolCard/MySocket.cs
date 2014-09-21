using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Sockets; 

namespace CoolCard
{
    class MySocket
    {
        private String host = CoolCard .Config .GetConfig("NETWORK", "host");
        private int port = Convert.ToInt32(CoolCard .Config .GetConfig("NETWORK", "port"));
        private int timeout = Convert.ToInt32(CoolCard.Config.GetConfig("NETWORK", "timeout")) * 1000;
        
        private Socket socket;
        protected  Socket Socket
        {
            set{socket = value;}
            get{return socket ;}
        }

        //建议Socket连接
        private  void Connect() 
        {
            //连接服务器主机
            this.socket = new Socket (AddressFamily.InterNetwork, SocketType.Stream, ProtocolType .Tcp );
            System.Net.IPAddress IP = System.Net .IPAddress .Parse (this.host);
            System.Net.IPEndPoint ipe = new System.Net.IPEndPoint(IP, port);
            this.socket.SendTimeout = timeout;
            this.socket.ReceiveTimeout = timeout;
            this.socket.Connect(ipe);
        }

        //关闭Socket连接
        private void Close()
        {
            //关闭Socket
            this.socket.Shutdown(SocketShutdown.Both);
            this.socket.Close();
        }


        //发送数据时只需调用此方法。连接会自动建立和关闭
        //返回服务器结果
        public String Send(String msg)
        {
            this.Connect();
            //向服务器主机发送信息           
            byte[] bytes_msg = new byte[4096];
            bytes_msg = Encoding.ASCII.GetBytes(msg+'\n');
            this.socket.Send(bytes_msg);
            //接收服务器返回
            String receive_string = "";
            byte[] bytes_receive = new byte[1024];
            int bytes = 0;
            while (true)
            {
                bytes = this.socket.Receive(bytes_receive, bytes_receive.Length, 0);
                if (bytes <= 0) break;
                receive_string += Encoding.ASCII.GetString(bytes_receive, 0, bytes);
                if (receive_string.Trim().Length != 0) break;
            }
            this.Close();

            return receive_string;
        }
    }
}
