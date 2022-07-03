# DDD in RESTful Flask example

# 開始之前

<br>

DDD (領域驅動設計) 是一種組織軟體的方式，最早是由 Eric Evans 在其同名書中所提出。

DDD 的重點在於以下三點 :

1. 專案的重點在於其核心領域 (Core Domain)，並以領域模型 (Domain Model) 為基礎來組織你的程式，其他的所有功能都是為了核心領域所服務
2. 領域模型並非由工程人員自己定義、建構，而是與領域專家或所有其他相關利益者共同產生並維護。
3. 由於領域模型是所有相關人員共同建置的，因此定義統一的語言就很重要。  
   記住，領域專家不想知道你的 CRUD，他們關注的是模型的操作、變化。

<br>
<br>

RESTful 是一種 API 的設計風格，最早由 Roy Fielding 在他的博士論文所提出。

REST 的重點在於以下三點 :

1. 資源 (Resource) 是由 Uri 來指定，也就是說每一個 Uri 都應該代表對 一組 ( 或一個 ) 資源的訪問
2. 對資源的操作包括取得、建立、修改和刪除，這些操作都正好對應 HTTP 協定提供的 GET、POST、PUT 和 DELETE 方法。
3. 資源並不是任何特定的資料 (尤其是不要認為它必須等於你 DB 的 Data)，而是你的系統所提供的任何可供 API 使用者訪問的內容，包含 文件、音樂、照片、影片等等。

<br>

### 簡單重點 :

DDD 關注的是 Domain Model 的建立，所有的行為都是對 Model 的操作 (Operation)。  
實體 (Entity) 清楚該如何操作自己的資料，有自己的行為。  
試想，你是一個人 (Entity)  
當你的老闆叫你開車去外地出差時，你收到了一個命令 (Command)。  
於是你自己開車 (行為) 去了某個地方。  
是你在控制自己的行為，並不是你的老闆 ( API ) 在操作著你，你並不是一個提線木偶。  
當有人給予你一個不可能 (或不該) 完成的任務時，Entity 必須是可以自己判斷此命令是否該執行的。

<br>

REST 關注的是使用一種易懂且直觀的方式來訪問你的資源 (CRUD)。  
他期望的是用簡單的 HTTP 動詞的 (GET、POST、PUT、DELETE)  
來對資源直接進行操作

<br>

這兩種方式乍看完全相反，但其實是很容易一起使用的。

<br>

本文將以最簡單的方式讓你了解如何建構一個以 DDD 為基礎的 RESTful Service  
我不會過度著墨於該如何 DDD，該如何建構模型。  
我也不會提到常與 DDD 一起使用的一些模式 (eg. CQRS, Event Sourcing) 等等  
這些模式常與 DDD 一起出現，是因為他們天生很適合一起使用。  
但並不代表他們 **必須** 一起使用

若你對這些內容很有興趣，  
這些資料在網路上非常豐富，你可以直接在網路上尋找，  
或你也可以直接購買 Eric Evans 的書來看。

<br>

# 讓我們開始吧

或許是得益於 Duck typing 的特性  
並且 DDD 的風格中過分強調 Domain Model 自己的行為能力  
DDD 在動態語言社群中的討論度遠遠低於靜態語言

但請記住，DDD 與任何程式語言無關，他只是一種組織你軟體的方法。  
並且由於動態語言的許多特性，我甚至認為他在動態語言中實施比靜態語言更簡單  
(但或許會比較要求開發人員主動遵守一些規範)。

DDD 自從被提出以來到現在會被大力推崇不是沒有原因的  
他已被多次證實可以很好的解決複雜系統的設計問題

下面，我將使用 python 與 Flask web framework 來示範一遍如何將 DDD 與 RESTful Service 進行結合

<br>

## Step.1 : 領域建模

---

DDD 的核心在於其領域模型 (Domain Model)  
所以我們首先從這開始

```
App
├─domain
│  └─model
│      └─ todo_task.py <- your model
...
...
```

今天我們的目標是設計一個 代辦事項 列表  
首先由需求方，或是說你的領域專家一起討論你的模型應該長什麼樣子

以代辦事項的領域來說  
每個代辦事項便是一個實體 (Entity)  
因此我們先建立一個代辦事項的最基本模型

<br>


```py
# todo_task.py
# ---

class Todo_Task():
    def __init__(self,  name: str) -> None:
        self.id: int = 0
        self.name: str = name
        self.status: bool = False
```

代辦事項的 Model 應該要包含至少兩個資料欄位

1. 代辦項目的名稱 : name
2. 代辦項目是否已完成 : status

接著領域專家向你提出  
嘿，我們的代辦項目應該要允許人們去變更此代辦事項的名字  
並且名字不該是空白的

於是我們加入該 Model 擁有的行為

```py
# todo_task.py
# ---

class Todo_Task():
    def __init__(self,  name: str) -> None:
        self.id: int = 0
        self.name: str = name
        self.status: bool = False

    def change_name(self, new_name: str):
        if (not new_name or not len(new_name)):
            raise ValueError("Cannot change to empty")
        self.name = new_name
        return self

    def change_task_status(self, isComplete: bool):
        self.status = bool(isComplete)
        return self

```

我們順便把改變狀態的操作也一併加進去  
如此一來，我們最基本的 Domain Model 就完成了

自此，領域專家們已經完成了他們的工作  
他們與你一同定義了 代辦事項 叫做 Todo_Task  
Todo_Task 可以 change_name 與 change_status

他們只關注領域內的內容，他們不想知道什麼是 CRUD，什麼是資料庫

你與領域專家一同建立的 Domain Model 現在有了自己的生命力，  
他不再是冷冰冰只為了儲存資料而存在的模型  
他可以更改自己的 完成狀態、名字  
且他也知道自己不能被改為空白的名字，知道自己的狀態一定要是布林值

<br>

## Step.2 : 建立你的基礎設施

---

基礎設施是用來讓你的軟體與外部程式溝通用的  
eg. Database、Event Bus 或是 其他 Microservice

我們首先建立一個 Repository Layer，由他來協助我們與 DB 溝通，  
這樣我們的其他功能就不需要知道與 DB 通訊需要什麼 Connection String，  
或是需要使用 PyMongo 等等之類的套件，這些功能全部交給 Repository 負責就好

```
App
├─domain
│  └─model
│      └─ todo_task.py
├─infrastructure
│  └─ taskRepository.py <- 專門負責訪問儲存 Todo_Task 的資料庫
│
...
...
```

在這裡，我建立了一個假的 DB 物件  
把資料全部存在內部記憶體

在真實的開發環境中，你可以藉由修改 taskRepository.py 中的 CRUD 程式碼來快速替換掉假 DB 至 真正的資料庫系統  
eg. Mongo , PostgreSQL 等等

在 taskRepository.py 外面的程式碼並不關注 DB 如何訪問，  
他們只知道呼叫 Repository 就可以存取 DB，所以你可以很方便地進行替換

```py
taskRepository.py
---

class TaskRepository():

    def __init__(self, ) -> None:
        self._context = database.get_collection('Todo_Tasks')

    def create(self, task: Todo_Task) -> Todo_Task:
        return self._context.create(task)

    def read(self, id: int) -> Todo_Task | None:
        data: Optional[Todo_Task] = self._context.read(id)
        return data

    def update(self, task: Todo_Task) -> Todo_Task:
        return self._context.update(task.id, task)

    def delete(self, id: int):
        self._context.delete(id)

    def list_all(self) -> list[Todo_Task]:
        return self._context.list_all()

```

有一個問題是，我是否該將我的 Domain Model 直接存入 Database ?  
答案是 **可以是也可以不是**

只要你的 Repository 知道如何將 Domain Model 轉換為 DB Model  
並且他也有能力將 DB Model 轉回 Domain Model 即可

Repository 以外的程式並不關注 Repository 如何存取資料，  
他們只知道他們可以透過 Repository 來與資料庫溝通

<br>

## Step.3 : 設計你的 RESTful API

---

REST 風格的 API 應該要能夠用 GET、POST、PUT、DELETE 的方式來訪問你的 Resource

```
App
├─domain
│  └─model
│      └─ todo_task.py
├─infrastructure
│  └─ taskRepository.py
│
├─router.py <- 用來指派 Uri 的路由
│
...
...
```

在我們這套系統中，唯一的資源只有 Todo_Task
於是我們在 router.py 中建立以下四個 Endpoint

```
router.py
---

task_router = Blueprint('Task', __name__)

@task_router.route('/tasks', methods=['GET'])
def list():
    ...

@task_router.route('/task', methods=['POST'])
def create():
    ...

@task_router.route('/task/<int:task_id>', methods=['PUT'])
def update(task_id: int):
    ...

@task_router.route('/task/<int:task_id>', methods=['DELETE'])
def delete(task_id: int):
    ...
```

當然，或許你覺得每次更新都要傳送整個 Todo_Task 的資料內容太過麻煩  
你也可以加入 PATCH 來更新部分資源  
或是加入嵌套的 Uri 來更新特定內容

```
@task_router.route('/task/<int:task_id>/name', methods=['PUT'])
def updata_name(task_id: int):
    ...

@task_router.route('/task/<int:task_id>/status', methods=['PUT'])
def update_status(task_id: int):
    ...
```

如此，我們充滿 RESTful 風格的 API Endpoint 就完成了  
讓我們繼續下一步

ps: 這裡我的 Router 直接使用了單個文件，當你的軟體複雜時，你當然可以把 Router 變為一個 Module 來進行規劃 (這實際上也是大多數 Web App 會使用的規劃方式)，  
這裡只是進行一個簡單示範  
當然，下面將要講到的 service.py 也是如此

<br/>

## Step.4 : 設計你的 Service Layer

---

接下來是我們的重頭戲，我們現在已經有了 API Endpoint  
但他還沒有實際內容

這些 Endpoint 看似是要直接操作 Todo_Task 的資料，  
他們的語意為直接對 Todo_Task 進行建立、修改、刪除的行為  
這看似違反了上面說的 Entity 中資料的修改應該由 Entity 自己進行

那我們實際上該如何融合他們呢?

這時 Service Layer 就派上用場了

```
App
├─domain
│  └─model
│      └─ todo_task.py
├─infrastructure
│  └─ taskRepository.py
├─router.py
├─service.py <-- 融合 API Enpoint、Domain Model 與 Repository 的工具
│
...
...
```

service.py 就是為我們融合這些東西的關鍵  
service layer 是 Domain 內與外的分界點

來自 Service 以外，呼叫 Service 的程式都是 Domain 以外的內容  
他們依靠呼叫 Service 來進行 Entity 的操作

我們先來看看 GET 方法

```
router.py
---
from service import get_all_tasks

@task_router.route('/tasks', methods=['GET'])
def list():
    tasks = get_all_tasks()
    return jsonify({
        "result": tasks
    })

```

負責處理 GET 方法的端點實際上並沒有做什麼事，  
他只是負責接收 User (client 端) 的請求，  
並將工作委派給 Service 來代為進行

接著我們看看 Service 做了什麼事

```
service.py
---

repo = TaskRepository()

def get_all_tasks() -> list[dict]:
    all_tasks = repo.list_all()
    return [{
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    } for task in all_tasks]

```

Service 收到了 get_all_tasks 的請求後，  
呼叫 Repo 將儲存的 Entities 取出，**並且** 將他轉了一手後再傳回給呼叫端  
這裡很重要的一點是資料的轉換

來自 Service 外部的人(程式)已經不再領域之內，**不要暴露** 你的 Domain Model 給外部知道  
Domain Model 包含很多關鍵資料，有些資料不是領域外的程式該知道的  
Service 代替他們訪問領域內部，並且回傳他們可以 (該) 知道的資料

這裡我直接用 Dict 回傳，在實際的設計中你可以另外設計屬於領域外的資料模型來做轉換

<br>

CREATE 與 DELETE 相對單純，我們跳到 PUT 來看看

```
router.py
---


@task_router.route('/task/<int:task_id>', methods=['PUT'])
def update(task_id: int):

    try:
        if get_body_value('id') != task_id:
            raise KeyError("body's id is not match path")

        name = get_body_value('name')
        if not isinstance(name, str):
            raise KeyError("'name' must be string")

        status_num = get_body_value('status')
        if (status_num == 1):
            status = True
        elif (status_num == 0):
            status = False
        else:
            raise KeyError("The value of status must be '1' or '2'")

        task = update_task(task_id, name, status)

        return jsonify({
            'result': task
        })
    except KeyError as msg:
        return msg.args[0], 400
    except:
        return '', 400

```

PUT 的 Endpoint 看似做了很多工作，  
但其實他只是在檢查輸入是否正確而已  
身為接受外部系統呼叫的直接窗口，這是屬於他的職責  
你也可以直接使用一些資料模型的套件 (eg. pydantic, marshmallow) 來進行  
如此你便可以減少很多程式碼

讓我們看看這個 Endpoint 最後做了什麼

```
    task = update_task(task_id, name, status)
```

他呼叫了 Service layer 中的 update_task 來進行資料的更新

讓我們轉進 service.py 來看看這邊做了什麼

```
service.py
---

def update_task(task_id: int, name: Optional[str] = None, status: Optional[bool] = None):
    task = repo.read(task_id)
    if not task:
        raise KeyError(f'Specific Task Id:{task_id} dose not exist.')

    if (name):
        task.change_name(name)
    if (status):
        task.change_task_status(status)

    task = repo.update(task)
    return {
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    }

```

首先，我們從 DB 中取出 User 指定的 Todo_Task (Entity)  
當資料不存在時，我們拋出一個錯誤來告知使用者

如果資料存在，我們觸發 Entity 中的 change_name 與 change_status 來更新資料

change_name 與 change_status 這兩個 Function 是你在 Step.1 時與 領域專家們 一起規劃好的，因此呼叫他們是很安全的事情。

<br>

千萬不要使用類似底下的程式碼來更新資料

```
    task.name = name
    task.status = status
```

當你試圖繞過 Domain Model 的定義的行為直接操作資料時，  
也就等於你正在嘗試繞過領域專家們的意見。  
記住，領域專家們之所以被稱作專家  
便是代表他們對這個領域比你熟悉，他們知道這個領域應該怎麼運作  
他們知道執行那些行為後會觸發哪些副作用  
以及他們知道執行這些行為後可能需要一起執行的一些功能

service layer 只定義了可以為客戶 (client) 做什麼，不應該替代 Entity 執行他的行為

最後我們將變更完畢的實體回存 DB

```
    task = repo.update(task)
    return {
        'id': task.id,
        'name': task.name,
        'status': 1 if task.status else 0
    }
```

並且像上面所說的 GET 一樣，重新包裝成領域外的內容回傳

<br>

### 小結 :

Service layer 的功能就是用來結合領域內與領域外的操作  
如果你已經習慣了 RESTful API 那種直接操作 Resource 的語意  
或許你可以這樣想

今天我 (User) 想了解關於我的個人資料，於是我向你(web app) GET 了一份關於我個人資料的文件  
在檢閱完了之後我發現關於我的身分證號碼有誤，  
於是我在我的 Local 端修改了正確的資料，並將這份文件的副本重新 PUT 給你，  
並 **建議** 你以此資料來更新關於我 (User) 的資訊  
如果整份資料太大，我或許也會使用 PATCH 或是 PUT User/id_number 等等方式來通知你

你在收到了我的資料後，將這份資料交給 Service Layer 進行處理，  
而 Service Layer 會使用 Domain Model 中定義的方法來操作 Entity  
如果成功，則返回新的資料並且回傳 Status 200  
若失敗，例如傳入新的身分證資料 E123456789，Entity 自己會知道這資料絕對是錯誤的 ( 因為身分證號碼也有其規則，而領域模型會知道這份規則是什麼 )  
於是從 Entity 中拋出一個錯誤  
最後你的 Endpoint 端點回傳 400 bad request 並指出錯誤的原因

<br>

## Step 5: 編寫你的測試

---

最後，別忘記撰寫 test case 來保護你的程式  
軟體發展的流程中，Domain Model 可能隨時改變  
撰寫測試來避免錯誤是絕對必要的

- 保護你的 Domain Model
- 保護你的 API 端點
- 確保你的 Service 用正確的方式服務以上兩者

<br>

```
test.test_api
  ✔️ test_create_endpoint_will_call_create_service
  ✔️ test_create_endpoint_will_return_400_if_missing_name
  ✔️ test_list_all_endpoint_will_call_get_all_tasks_service
  ✔️ test_update_endpoint_will_call_update_service
  ✔️ test_update_endpoint_will_return_400_if_target_not_found
  ✔️ test_update_particular_member_of_task_will_call_update_service_with_name_parameter
  ✔️ test_update_particular_member_of_task_will_call_update_service_with_status_parameter
  ✔️ test_delete_endpoint_will_call_delete_service
test.test_domain
  ✔️ test_task_change_name_will_success
  ✔️ test_task_cannot_change_invalid_name
  ✔️ test_task_change_status
test.test_service
  ✔️ test_create_new_task_will_save_to_repo
  ✔️ test_update_task_will_save_into_repo
  ✔️ test_update_task_will_raise_error_if_task_id_not_exist
  ✔️ test_delete_task_will_delete_from_repo
  ✔️ test_list_all_will_get_from_repo
```

<br>

以上，就是以最簡單的方式結合 DDD 與 RESTful API 的方法

<br>

# 寫在最後

DDD 不是萬靈丹，他無法神奇的突然解決你的問題  
對於小型系統而言，他甚至會增加許多不必要的複雜性

**謹慎的選擇你是否需要導入 DDD**

請為了 **需要** 而使用 工具、技術，而不是 **為了使用而使用**

若有謬誤，請多包涵並懇請您提出，我會盡速修正

<br>
<br>
<br>
