答题接口和答题器之间的通讯协议

数据结构定义:

// 答题类型 对应于FaqRequestPacket中的request\_type  
#define REQUEST\_TYPE\_POS  
0          
// 坐标  
#define REQUEST\_TYPE\_ABCD  1          
// 选项  
#define REQUEST\_TYPE\_OTHER 2          
// 文本  
#define REQUEST\_TYPE\_DOUBLE\_POS 3      // 双坐标

#pragma
pack(push) //保存对齐状态  
#pragma pack(4)//设定为4字节对齐

// 发送包结构体  
typedef struct  
{  
    // 服务器转发用(分流的时候可能会用到)  
    SOCKET socket;              
// 分流上级发送的socket id.  
    char  ip[32];               
// 分流上级机器IP

// 客户端内容  
    DWORD request\_type; // 答题类型  
    DWORD data\_len;     // 真实数据的长度  
    char  data[1];      // 数据指针.  
}FaqRequestPacket;

// 接收包结构体  
typedef struct  
{  
    // 服务器转发用  
    SOCKET socket;        
// 同FaqRequestPacket  
    char  ip[32];         
// 同FaqRequestPacket

// 客户端内容  
    char result[256];      // 接收到的答案. 文本形式描述.   
}FaqReceivePacket;

#pragma
pack(pop)//恢复对齐状态

通讯过程流程描述

发送数据包详细格式解析:

发送的数据包由包头+数据体
两部分组成.

其中包头的长度是sizeof(FaqRequestPacket).

数据体的长度是FaqRequestPacket结构体中data\_len指定的长度. 用图形描述如下:

                             
整个数据包(发送)

   

        FaqRequestPacket(12字节)  |    数据(数据头+数据体)

      长度sizeof(FaqRequestPacket)        长度(data\_len)

其中数据部分的结构定义如下:

数据部分包含2部分，数据头和数据体.  
数据头12个字节. 前4个字节是一个头标识. 内容是4个字符 'D' 'M' 'F' 'Q'.  
接下来4个字节的内容表示当前图像有多少帧. 如果是静态图像此值为1或者65535. (65535表示是BMP图像数据，65534表示是TXT文字数据(文字编码是GBK))  
再接下来4个字节表示每帧之间的延时是多少毫秒. 如果是静态图像此值为0

数据体部分是连续顺序存放图片数据. 按照帧的顺序依次存放. 每个帧前的4个字节表示当前帧有多少个字节.比如  
(长度)帧数1(长度)帧数2……(长度)帧数N.   每个帧的图像格式是jpeg或者bmp格式,或者是TXT文字数据  
  
综上,发送包总的长度描述如下:  
12字节(sizeof(FaqRequestPacket)) + 12字节(数据头) + 4字节(第一帧长度) + (第一帧数据) + 4字节(第二帧长度) + (第二帧数据) + ….

接收包的格式很简单。就不多说了.

注意的是，以上只是接收和发送的纯数据格式. 真正发送时，还会在包头加上序列号，长度等校验信息. 以下是我用到的发送和接收数据的函数源码. 其他语言也可以参考.

// Common Return Code.

#define RET\_SUCCESS                                  1

#define RET\_FAIL                                 -1

#define RET\_NET\_NOT\_INIT                         -2

#define RET\_NO\_ERROR                             1

#define RET\_ACCEPT\_SOCKET\_ERROR                      -1

#define RET\_CLIENT\_SOCKET\_ERROR                      -2

#define RET\_NO\_SOCKET                                -3

#define RET\_NO\_CONNECTION                            -4

#define RET\_SOCKET\_CLOSED                            0

#define RET\_TIMEOUT                                  -5

#define RET\_SOCKET\_SHUT\_DOWN                         -6

#define RET\_SERVER\_NOT\_PREPARED                      -7

#define RET\_SOCKET\_NO\_ORDER                          -8

#define RET\_CONNECT                                  -9

#define RET\_DISCONNECT                               -10

#define RET\_NO\_AVAILABLE\_PEER                        -11

#define RET\_NO\_PEER                                  -12

#define RET\_NO\_PACKAGE                               -13

#define READ\_TIMEOUT                             5000

#define WRITE\_TIMEOUT                                5000

#define READ\_UNIT\_SIZE                        512
// less than general MTU size.

#define WRITE\_UNIT\_SIZE                       512
// less than general MTU size.

#define MSG\_LEN\_INFO\_SIZE                     4

#define MAX\_NET\_TRIAL                         30

#define CHECK\_ALIVE\_VALUE                     -987654321

#define MAX\_RECV\_AGAIN                        3

int TCPRead(SOCKET Socket,
char \*Buffer, DWORD BufferSize, DWORD TimeoutMilli, DWORD \*ErrorCode)

{

    BOOL
bError;

    int ReturnCode;

    char
LenInfo[MSG\_LEN\_INFO\_SIZE];

    int RetLen;

    char
ReadBuff[READ\_UNIT\_SIZE];

    DWORD
CopyingSize;

    int ResRecv;

    int Timeout;

    char
\*pReadingPoint;

    int ToReadSize;

    int UnitReadSize;

    int TimeoutOld;

    int OutLen;

    int LoopCount;

    int RecvAgainCount;

    bError = 0;

    ReturnCode = RET\_FAIL;

    TimeoutOld = -1;

    if
(0 > Socket || 0 == ErrorCode)

    {

       bError = 1;

       ReturnCode = RET\_FAIL;

       goto ErrHand;

    }

    \*ErrorCode = 0;

    OutLen = sizeof (TimeoutOld);

    if
(SOCKET\_ERROR == getsockopt(Socket, SOL\_SOCKET,
SO\_RCVTIMEO, (char \*)&TimeoutOld, &OutLen))

    {

       \*ErrorCode = WSAGetLastError();

       bError = 1;

       ReturnCode = RET\_FAIL;

       goto ErrHand;

    }

    Timeout
= TimeoutMilli; // Assigning is due to input the
address of the Timeout. 0 = infinite.

    if
(SOCKET\_ERROR == setsockopt(Socket, SOL\_SOCKET,
SO\_RCVTIMEO, (char \*)&Timeout, sizeof (Timeout)))

    {

       \*ErrorCode = WSAGetLastError();

       bError = 1;

       ReturnCode = RET\_FAIL;

       goto ErrHand;

    }

    if
(0 == Buffer || 0 == BufferSize)

    {

RecvAgainNew:    

       RecvAgainCount = 0;

RecvAgain:

       ZeroMemory(LenInfo, sizeof (LenInfo));

       ResRecv = recv(Socket, LenInfo, sizeof (LenInfo), MSG\_PEEK);

       if
(SOCKET\_ERROR == ResRecv)

       {

           \*ErrorCode = WSAGetLastError();

          

           if
(WSAECONNRESET == \*ErrorCode || WSAECONNABORTED == \*ErrorCode || WSAESHUTDOWN == \*ErrorCode
|| WSAENETRESET == \*ErrorCode)

           {

              bError = 1;

              ReturnCode = RET\_SOCKET\_SHUT\_DOWN;

              goto ErrHand;

           }

           else
if (WSAETIMEDOUT == \*ErrorCode)

           {

              bError = 1;

              ReturnCode = RET\_TIMEOUT;

              goto ErrHand;

           }

          

           bError = 1;

           ReturnCode = RET\_FAIL;

           goto ErrHand;

       }

       else
if (0 == ResRecv) // socket closed.

       {

           bError = 1;

           ReturnCode = RET\_SOCKET\_CLOSED;

           goto ErrHand;

       }

       else
if (sizeof (LenInfo) > ResRecv)

       {

           if
(MAX\_RECV\_AGAIN <= RecvAgainCount)

           {

              bError = 1;

              ReturnCode = RET\_FAIL;

              goto ErrHand;

           }

           RecvAgainCount++;

           goto RecvAgain;

       }

       else
if (sizeof (LenInfo) != ResRecv)

       {

           bError = 1;

           ReturnCode = RET\_FAIL;

           goto ErrHand;

       }

       else

       {

           memcpy(&RetLen, LenInfo, sizeof (LenInfo));

           if
(CHECK\_ALIVE\_VALUE == RetLen)

           {

              ResRecv = recv(Socket, LenInfo, sizeof (LenInfo), 0); // recv() may
return arbitrary value. <- but it can handle the size of data as much as
MTU.

              if
(SOCKET\_ERROR == ResRecv)

              {

                  \*ErrorCode = WSAGetLastError();

                 

                  if
(WSAECONNRESET == \*ErrorCode || WSAECONNABORTED == \*ErrorCode || WSAESHUTDOWN == \*ErrorCode
|| WSAENETRESET == \*ErrorCode)

                  {

                     bError = 1;

                     ReturnCode = RET\_SOCKET\_SHUT\_DOWN;

                     goto ErrHand;

                  }

                  else
if (WSAETIMEDOUT == \*ErrorCode)

                  {

                     bError = 1;

                     ReturnCode = RET\_TIMEOUT;

                     goto ErrHand;

                  }

                 

                  bError = 1;

                  ReturnCode = RET\_FAIL;

                  goto ErrHand;

              }

              else
if (0 == ResRecv) // socket closed.

              {

                  bError = 1;

                  ReturnCode = RET\_SOCKET\_CLOSED;

                  goto ErrHand;

              }

              goto RecvAgainNew;

           }

           else
if (0 >= RetLen)

           {

              bError = 1;

              ReturnCode = RET\_SOCKET\_NO\_ORDER;

              goto ErrHand;

           }

           else

           {

              bError = 0;

              ReturnCode = RetLen;

              goto ErrHand;

           }

       }

    }

    else
// read the data.

    {

       CopyingSize = 0;

       LoopCount = 0;

       ToReadSize = BufferSize + sizeof (LenInfo);

       while
(1)

       {

           if
(sizeof (ReadBuff) <= ToReadSize)

           {

              UnitReadSize = sizeof (ReadBuff);

           }

           else

           {

              UnitReadSize = ToReadSize;

           }

           ZeroMemory(ReadBuff, sizeof (ReadBuff));

           pReadingPoint = ReadBuff;

           ResRecv = recv(Socket, pReadingPoint, UnitReadSize, 0);

           if
(SOCKET\_ERROR == ResRecv)

           {

              \*ErrorCode = WSAGetLastError();

              if
(WSAECONNRESET == \*ErrorCode || WSAECONNABORTED == \*ErrorCode || WSAESHUTDOWN == \*ErrorCode
|| WSAENETRESET == \*ErrorCode)

              {

                  bError = 1;

                  ReturnCode = RET\_SOCKET\_SHUT\_DOWN;

                  goto ErrHand;

              }

              else
if (WSAETIMEDOUT == \*ErrorCode)

              {

                  bError = 1;

                  ReturnCode = RET\_TIMEOUT;

                  goto ErrHand;

              }

              bError = 1;

              ReturnCode = RET\_FAIL;

              goto ErrHand;

           }

           else
if (0 == ResRecv) // socket closed.

           {

              bError = 1;

              ReturnCode = RET\_SOCKET\_CLOSED;

              goto ErrHand;

           }

           else

           {

              if
(0 == LoopCount)

              {

                  memcpy(Buffer + CopyingSize, ReadBuff + sizeof (LenInfo), ResRecv - sizeof (LenInfo));

                  CopyingSize += ResRecv - sizeof (LenInfo);

              }

              else

              {

                  memcpy(Buffer + CopyingSize, ReadBuff, ResRecv);

                  CopyingSize += ResRecv;

              }

              LoopCount++;

              ToReadSize -= ResRecv;

              if
(0 >= ToReadSize)

              {

                  break;

              }

           }

       }

       bError = 0;

       ReturnCode = CopyingSize;

       goto ErrHand;

    }

ErrHand:

    if
(-1 != TimeoutOld)

    {

       Timeout
= TimeoutOld;

       if
(SOCKET\_ERROR == setsockopt(Socket, SOL\_SOCKET,
SO\_RCVTIMEO, (char \*)&Timeout, sizeof (Timeout)))

       {

           \*ErrorCode = WSAGetLastError();

           bError = 1;

           ReturnCode = RET\_FAIL;

           goto ErrHand;

       }

    }

    return
ReturnCode;

} // TCPRead()

int TCPWrite(SOCKET Socket,
char \*Buffer, DWORD BufferSize, DWORD TimeoutMilli, DWORD \*ErrorCode)

{

    BOOL
bError;

    int ReturnCode;

    DWORD
WritingSize;

    int ResSend;

    int Timeout;

    int TimeoutOld;

    int OutLen;

    int ToSendSize;

    int ToSendSizeUnit;

    int RemainedUnit;

    int Loop;

    int SendingNumber;

    char
\*pIndex;

    char
WriteBuf[WRITE\_UNIT\_SIZE];

    char
\*pIndexUnit;

    bError = 0;

    ReturnCode = RET\_FAIL;

    TimeoutOld = -1;

    if
(0 > Socket || 0 == Buffer || 0 == BufferSize || 0
== ErrorCode)

    {

       bError = 1;

       ReturnCode = RET\_FAIL;

       goto ErrHand;

    }

    \*ErrorCode = 0;

    OutLen = sizeof (TimeoutOld);

    if
(SOCKET\_ERROR == getsockopt(Socket, SOL\_SOCKET,
SO\_SNDTIMEO, (char \*)&TimeoutOld, &OutLen))

    {

       \*ErrorCode = WSAGetLastError();

       bError = 1;

       ReturnCode = RET\_FAIL;

       goto ErrHand;

    }

    Timeout
= TimeoutMilli; // Assigning is due to input the
address of the Timeout. 0 = infinite.

    if
(SOCKET\_ERROR == setsockopt(Socket, SOL\_SOCKET,
SO\_SNDTIMEO, (char \*)&Timeout, sizeof (Timeout)))

    {

       \*ErrorCode = WSAGetLastError();

       bError = 1;

       ReturnCode = RET\_FAIL;

       goto ErrHand;

    }

    SendingNumber = ((BufferSize + sizeof (BufferSize)) /
WRITE\_UNIT\_SIZE) + ((0 != ((BufferSize + sizeof (BufferSize)) %
WRITE\_UNIT\_SIZE)) ? 1 : 0);

    WritingSize = 0;

    pIndex = Buffer;

    ToSendSize = BufferSize;

    for
(Loop = 0; Loop < SendingNumber; Loop++)

    {

       if
(0 == Loop)

       {

           ZeroMemory(WriteBuf, sizeof (WriteBuf));

           ToSendSizeUnit = ((WRITE\_UNIT\_SIZE - sizeof
(BufferSize)) > ToSendSize)
? ToSendSize : WRITE\_UNIT\_SIZE - sizeof
(BufferSize);

           memcpy(WriteBuf, &BufferSize, sizeof (BufferSize));

           memcpy(WriteBuf + sizeof (BufferSize), pIndex, ToSendSizeUnit);

           pIndex += ToSendSizeUnit;

           ToSendSize -= ToSendSizeUnit;

           ToSendSizeUnit += sizeof (BufferSize); // compensation.

       }

       else

        {

           ZeroMemory(WriteBuf, sizeof (WriteBuf));

           ToSendSizeUnit = (WRITE\_UNIT\_SIZE > ToSendSize)
? ToSendSize : WRITE\_UNIT\_SIZE;

           memcpy(WriteBuf, pIndex, ToSendSizeUnit);

           pIndex += ToSendSizeUnit;

           ToSendSize -= ToSendSizeUnit;

       }

       RemainedUnit = ToSendSizeUnit;

       pIndexUnit = WriteBuf;

       while
(0 < RemainedUnit)

       {

           ResSend = send(Socket, pIndexUnit,
RemainedUnit, 0); // send() operates as all or
nothing.

           if
(SOCKET\_ERROR == ResSend)

           {

              \*ErrorCode = WSAGetLastError();

             

              if
(WSAECONNRESET == \*ErrorCode || WSAECONNABORTED == \*ErrorCode || WSAESHUTDOWN == \*ErrorCode
|| WSAENETRESET == \*ErrorCode)

              {

                  bError = 1;

                  ReturnCode = RET\_SOCKET\_SHUT\_DOWN;

                  goto ErrHand;

              }

              else
if (WSAETIMEDOUT == \*ErrorCode)

              {

                  bError = 1;

                  ReturnCode = RET\_TIMEOUT;

                  goto ErrHand;

              }

             

              bError = 1;

              ReturnCode = RET\_FAIL;

              goto ErrHand;

           }

           else
if (0 == ResSend) // socket closed.

           {

              bError = 1;

              ReturnCode = RET\_SOCKET\_CLOSED;

              goto ErrHand;

           }

           else
if (ResSend == RemainedUnit)
// the normal case.

           {

              WritingSize += ResSend;

              RemainedUnit -= ResSend;

           }

           else
if (ResSend > RemainedUnit)

           {

              bError = 1;

              ReturnCode = RET\_FAIL;

              goto ErrHand;

           }

           else
if (ResSend < RemainedUnit)

           {

              WritingSize += ResSend;

              RemainedUnit -= ResSend;

              pIndexUnit += ResSend;

           }

           else
// what? error.

           {

              bError = 1;

              ReturnCode = RET\_FAIL;

              goto ErrHand;

           }

       }

    }

ErrHand:

    if
(-1 != TimeoutOld)

    {

       Timeout
= TimeoutOld;

       if
(SOCKET\_ERROR == setsockopt(Socket, SOL\_SOCKET,
SO\_SNDTIMEO, (char \*)&Timeout, sizeof (Timeout)))

       {

           \*ErrorCode = WSAGetLastError();

           bError = 1;

           ReturnCode = RET\_FAIL;

       }

    }

    if
(1 == bError)

    {

       return
ReturnCode;

    }

    ReturnCode = WritingSize - sizeof (BufferSize);

    return
ReturnCode;

} // TCPWrite()