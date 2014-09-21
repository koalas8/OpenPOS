using System;
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Text;
using System.Data;
using CardGenerator;
using Npgsql;

namespace CardGenerator
{
    public class Generator
    {
        public const String SUCCESS = "0";
        public const String ERROR = "1";
        public const String UNIT_DONOT_EXIST = "2";

        /// <summary>
        /// 获取集团本批次的发卡批次号
        /// </summary>
        /// <param name="unitNum">集团编号</param>
        /// <returns>本批次的发卡批次号</returns>
        public static int GetCurrentBatchNum(String unitNum)
        {
            DB db = new DB();
            DataTable dt = new DataTable();
            dt = db.GetData(String.Format("SELECT start_batch_no FROM card_resource WHERE unit_no = '{0}'", unitNum));
            db.Conn.Close();

            return (int)dt.Rows[0]["start_batch_no"];
        }

        /// <summary>
        /// 获取给定集团的发卡起始号
        /// </summary>
        /// <param name="unitNum"></param>
        /// <returns></returns>
        public static int GetStartCardNum(String unitNum)
        {
            DB db = new DB();
            DataTable dt = new DataTable();
            dt = db.GetData(String.Format("SELECT start_card_no FROM card_resource WHERE unit_no = '{0}'", unitNum));
            db.Conn.Close();
            return (int)dt.Rows[0]["start_card_no"];
        }


        /// <summary>
        /// 获取可以生成制卡文件的批次号
        /// </summary>
        /// <param name="generatedFileFlag">是否获取已生成制卡文件的批次号的标志</param>
        /// <returns></returns>
        public static ArrayList GetAllBatchNums(String unitNum, Boolean generatedFileFlag, Boolean notGeneratedFileFlag)
        {
            String sql = String.Format("SELECT DISTINCT(batch_no) FROM card_batch_info WHERE unit_no = '{0}'", unitNum);
            if (generatedFileFlag)
            {
                sql = sql + " AND (file_generated = true";
            }
            else 
            {
                sql = sql + " AND (file_generated = false";
            }

            if (notGeneratedFileFlag)
            {
                sql = sql + " OR file_generated = false)";
            }
            else
            {
                sql = sql + " OR file_generated = true)";
            }

            DataTable dt = new DataTable();
            DB db = new DB();
            ArrayList batchNumArray = new ArrayList();
            dt = db.GetData(sql);
            foreach (DataRow dr in dt.Rows)
            {
                batchNumArray.Add(dr[0]);
            }
            return batchNumArray;
        }


        /// <summary>
        /// 生成卡数据并写入到数据库
        /// </summary>
        /// <param name="bin">卡BIN</param>
        /// <param name="unitNum">发卡集团号，4位</param>
        /// <param name="cardKind">卡类型：0－储值卡，1－储次卡</param>
        /// <param name="depositFlag">是否可充值标志</param>
        /// <param name="passwordFlag">是否有密码标志</param>
        /// <param name="randomPasswordFlag">对于每张卡是否生成随机密码</param>
        /// <param name="password">初始密码</param>
        /// <param name="amount">初始金额</param>
        /// <param name="points">初始积分</param>
        /// <param name="pointsRule">积分规则</param>
        /// <param name="validLife">有效期（月）</param>
        /// <param name="cardCount">发卡数量</param>
        /// <returns></returns>
        public static String GenerateCards(String bin, String unitNum, String cardKind, Boolean depositFlag, Boolean passwordFlag,
            Boolean randomPasswordFlag,String password, int amount, int points, int pointsRule, int validLife, int cardCount, String remark)
        {
            ArrayList arrayCards = new ArrayList();
            DB db = new DB();
            DataTable dt = new DataTable();
            dt = db.GetData(String.Format("SELECT * FROM card_resource WHERE unit_no = '{0}'", unitNum));
            int startCardNum = (int)dt.Rows[0]["start_card_no"];
            int startBatchNum = (int)dt.Rows[0]["start_batch_no"];

            String pwdFlag = "0";
            // String depFlag = "0";
            if (passwordFlag) {  pwdFlag = "1"; }            
            // if (depositFlag) { depFlag = "1"; }

            for (int i = 0; i < cardCount; i++)
            {
                Card card = new Card();
                // card.CardNum = bin + unitNum + cardKind + depFlag + pwdFlag + Utils.zfill((startCardNum+i).ToString(), 8);
                card.CardNum = bin + unitNum + pwdFlag + Utils.zfill((startCardNum + i).ToString(), 10);
                card.Amount = amount;
                card.Rechargable = depositFlag;
                card.CardKind = cardKind;
                card.Points = points;
                card.PointsRule = pointsRule;
                card.Unit = unitNum;
                card.ValidLife = validLife;
                card.BatchNum = startBatchNum;
                card.Track2 = card.CardNum + "=4912220" + Utils.random(11);
                if (passwordFlag)
                {
                    card.Password = randomPasswordFlag ? Utils.random(6) : password;
                }
                else
                {
                    card.Password = "";
                }

                arrayCards.Add(card);
            }

            // 将生成的卡信息写入到数据库
            if (arrayCards.Count > 0)
            {
                db.Conn.Open();
                String sql = "";
                NpgsqlTransaction transaction = db.Conn.BeginTransaction();
                foreach (Card card in arrayCards)
                {
                    sql = String.Format("INSERT INTO tmp_card_info(card_no,track_2,password,status,amount,points_rule, points,unit_no,valid_life,batch_no, card_kind, recharge_flag) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}', '{10}', '{11}')",
                            card.CardNum, card.Track2, card.Password, "0", card.Amount, card.PointsRule, card.Points, card.Unit, card.ValidLife, card.BatchNum, card.CardKind, card.Rechargable);
                    db.ExecSql(sql);
                }

                Card c = (Card)arrayCards[arrayCards.Count - 1];

                sql = String.Format("UPDATE card_resource SET start_card_no={0}, start_batch_no={1} WHERE unit_no='{2}'",
                    Convert.ToInt32(c.CardNum.Substring(10)) + 1, c.BatchNum + 1, c.Unit);
                db.ExecSql(sql);

                sql = String.Format("INSERT INTO card_batch_info (batch_no, file_generated, unit_no, remark) VALUES ({0}, false, '{1}', '{2}')", Convert.ToInt32(c.BatchNum), c.Unit, remark);
                db.ExecSql(sql);

                transaction.Commit();
                db.Conn.Close();
            }
            return SUCCESS;
        }


        // 查询制卡文件
        public static DataTable QueryGenFile(String unitNum, int batchNum)
        {
            DataTable dt = new DataTable();
            DB db = new DB();
            dt = db.GetData(String.Format("SELECT card_no, track_2, password, valid_life FROM tmp_card_info WHERE batch_no={0} AND unit_no='{1}'", batchNum, unitNum));
            return dt;
        }

        /// <summary>
        // 生成制卡文件后要提交数据库,某集团的某批次已制卡完成
        /// </summary>
        /// <param name="unitNum"></param>
        /// <param name="batchNum"></param>
        /// <returns></returns>
        public static Boolean CommitGenFile(String unitNum, int batchNum)
        {
            DB db = new DB();
            db.Conn.Open();
            NpgsqlTransaction transaction = db.Conn.BeginTransaction();            
            //DataTable dt = new DataTable();
            long count = db.GetCount(String.Format("SELECT COUNT(*) FROM card_batch_info WHERE file_generated=true AND unit_no='{0}' AND batch_no={1}", unitNum, batchNum));
            if (count == 0)
            {
                // card_kind: 卡类型 0：磁条卡 1：IC接解卡 2：IC非接触
                // card_type: 卡种类 0：系统卡 1：自发卡                
                db.ExecSql(String.Format("INSERT INTO card_info(card_no, card_kind, password, status, amount, points_rule, exp_date, points, unit_no, track_2, valid_life, card_type) (SELECT card_no, card_kind, md5(password), status, amount, points_rule, exp_date, points, unit_no, track_2, valid_life, '0' FROM tmp_card_info WHERE unit_no = '{0}' AND batch_no = {1})", unitNum, batchNum));
                db.ExecSql(String.Format("UPDATE card_batch_info SET file_generated=true WHERE unit_no='{0}' AND batch_no={1}", unitNum, batchNum));
            }
            transaction.Commit();
            db.Conn.Close();
            return true;
        }

        /// <summary>
        /// 获取所有集团号和集团名称，并根据集团号或集团名称排序。
        /// </summary>
        /// <param name="orderByUnitNum">是否根据集团号排序，默认为是。如果为否，则根据集团名称排序。</param>
        /// <returns></returns>
        public static ArrayList GetAllUnits(Boolean orderByUnitNum=true)
        {
            DataTable dt = new DataTable();
            DB db = new DB();
            ArrayList arrayList = new ArrayList();
            String sql = "";
            if (orderByUnitNum)
            {
                sql = "SELECT unit_no, unit_name FROM unit_info WHERE status='0' ORDER BY unit_no";
            }
            else
            {
                sql = "SELECT unit_no, unit_name FROM unit_info WHERE status='0' ORDER BY unit_name";
            }
            dt = db.GetData(sql);
            foreach (DataRow dr in dt.Rows)
            {
                arrayList.Add(dr["unit_no"] + "-" + dr["unit_name"]);
            }
            return arrayList;
        }
    }
}
