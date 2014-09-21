using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace CardGenerator
{
    class Card
    {
        private String _cardNum;

        public String CardNum
        {
            get { return _cardNum; }
            set { _cardNum = value; }
        }
        private String _unit;

        public String Unit
        {
            get { return _unit; }
            set { _unit = value; }
        }
        private String _cardKind;

        public String CardKind
        {
            get { return _cardKind; }
            set { _cardKind = value; }
        }
        private Boolean _passwordFlag;

        public Boolean PasswordFlag
        {
            get { return _passwordFlag; }
            set { _passwordFlag = value; }
        }
        private int _amount;

        public int Amount
        {
            get { return _amount; }
            set { _amount = value; }
        }
        private String _password;

        public String Password
        {
            get { return _password; }
            set { _password = value; }
        }
        private int _validLife;

        public int ValidLife
        {
            get { return _validLife; }
            set { _validLife = value; }
        }
        private int _points;

        public int Points
        {
            get { return _points; }
            set { _points = value; }
        }
        private int _pointsRule;

        public int PointsRule
        {
            get { return _pointsRule; }
            set { _pointsRule = value; }
        }

        private int _batchNum;

        public int BatchNum
        {
            get { return _batchNum; }
            set { _batchNum = value; }
        }

        private String _track2;

        public String Track2
        {
            get { return _track2; }
            set { _track2 = value; }
        }

        private Boolean _depositFlag;

        public Boolean DepositFlag
        {
            get { return _depositFlag; }
            set { _depositFlag = value; }
        }

        private Boolean rechargable;

        public Boolean Rechargable
        {
            get { return rechargable; }
            set { rechargable = value; }
        }
    }
}
