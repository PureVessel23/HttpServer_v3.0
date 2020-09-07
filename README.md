# Http Server v3.0

## 功能

HttpServer 部分：

- 获取 Http 请求
- 解析 Http 请求
- 将请求发送给 WebFrame
- 从 WebFrame 接收反馈数据
- 将数据组织为 Responce 格式发送给客户端

WebFrame 部分：

- 从 HttpServer 接收具体请求
- 根据请求进行逻辑处理和数据处理
- 将需要的数据反馈给 HttpServer

特点：

- 采用 HttpServer 和应用处理分离的模式，降低了耦合度
- 采用了用户配置文件的思路
- WebFrame 部分采用了模拟后端框架的处理方法

技术点：

- HttpServer 部分需要与两端建立通信
- WebFrame 部分采用多路复用接收并发请求
- 数据传递使用 json 格式

#### 项目结构

project

- httpserver
  - HttpServer.py（主程序）
  - config.py（HttpServer 配置）
- webframe
  - WebFrame.py（主程序代码）
  - static（存放静态网页）
  - views.py（应用处理程序）
  - urls.py（存放路由）
  - settings.py（框架配置）

#### 交互数据格式协议

HttpServer -> WebFrame：{method:'GET', info:'/'}

WebFrame -> HttpServer：{status:'200', data:'data'}

