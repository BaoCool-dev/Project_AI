# GIỚI THIỆU BÀI TOÁN 8-PUZZLE
Bài toán 8-Puzzle là một trò chơi trượt ô trên lưới 3x3, gồm 8 ô chứa số từ 1 đến 8 và một ô trống. Mục tiêu là di chuyển các ô để đưa trạng thái ban đầu về trạng thái mục tiêu theo thứ tự từ 1 đến 8, với ô trống ở cuối cùng. Đây là bài toán cổ điển trong trí tuệ nhân tạo, dùng để đánh giá hiệu quả các thuật toán tìm kiếm.
# 1. MỤC TIÊU
Mục tiêu của dự án 8-Puzzle là xây dựng một hệ thống giải bài toán 8-Puzzle bằng nhiều thuật toán trí tuệ nhân tạo khác nhau, nhằm so sánh hiệu quả giữa các phương pháp tìm kiếm truyền thống, heuristic, tối ưu hóa và học tăng cường. Qua đó, người dùng có thể trực quan hóa quá trình giải, đánh giá ưu nhược điểm của từng thuật toán và ứng dụng vào các bài toán ra quyết định, lập kế hoạch hoặc xử lý không chắc chắn.
# 2. NỘI DUNG
## 2.1 Nhóm thuật toán tìm kiếm không có thông tin (Uninformed Search Algorithms)
### Các thành phần chính của bài toán tìm kiếm:
- Trạng thái ban đầu:
    Lưới 3x3 gồm các số từ 1 đến 8 và một ô trống (được biểu diễn bằng số 0). Trạng thái bắt đầu cụ thể là:
[[1, 2, 3], [4, 6, 0], [7, 5, 8]]

- Trạng thái mục tiêu:
    Lưới được sắp xếp theo thứ tự tăng dần với ô trống nằm ở cuối: [[0, 1, 3], [4, 2, 5], [7, 8, 6]]

- Không gian trạng thái:
    Bao gồm tất cả các hoán vị hợp lệ của 9 ô trong lưới 3x3 mà có thể đạt được thông qua di chuyển ô trống theo luật chơi.

- Hành động:
    Tại mỗi bước, ô trống có thể dịch chuyển sang trái, phải, lên hoặc xuống nếu còn trong giới hạn lưới, từ đó tạo ra trạng thái mới.

- Chi phí:
    Mỗi thao tác di chuyển ô trống được tính với chi phí bằng 1 đơn vị.

### Giải pháp:
- Tìm dãy bước di chuyển từ trạng thái ban đầu đến trạng thái mục tiêu thông qua các thuật toán tìm kiếm không có thông tin như: BFS, DFS, UCS, IDS. Các thuật toán này duyệt không gian trạng thái để tìm đường đi hợp lệ.

### Hình ảnh gif của từng thuật toán:

### BFS

![Image](https://github.com/user-attachments/assets/0232eaec-6c49-4eb9-90af-69057ad96642)

### DFS

![Image](https://github.com/user-attachments/assets/7329f0cf-65cb-4fb4-9914-4ef5e9c7cffe)

### UCS

![Image](https://github.com/user-attachments/assets/f6b829e6-e932-4927-9a70-6fb54c689ecb)

### IDS

![Image](https://github.com/user-attachments/assets/478b00ae-f617-4504-af10-b718c7391bbe)


### Đánh giá các thuật toán:

- Breadth-First Search (BFS): BFS mở rộng các trạng thái theo từng tầng, đảm bảo tìm được lời giải ngắn nhất khi chi phí mỗi bước là như nhau. Tuy nhiên, do phải lưu toàn bộ trạng thái cùng cấp độ, lượng bộ nhớ tiêu tốn tăng theo cấp số nhân theo độ sâu, gây khó khăn khi giải quyết bài toán có không gian lớn và sâu.

- Depth-First Search (DFS): DFS ưu tiên đi sâu vào từng nhánh trước khi quay lại nhánh khác, nên sử dụng bộ nhớ rất ít vì chỉ lưu trạng thái trên một nhánh duy nhất. Tuy nhiên, nó có thể dẫn đến duyệt vô hạn nếu gặp vòng lặp hoặc nhánh không có lời giải, và thường không tìm được lời giải ngắn nhất nếu không kiểm soát độ sâu hoặc không đánh dấu trạng thái đã xét.

- Uniform-Cost Search (UCS): UCS luôn chọn mở rộng trạng thái có chi phí tích lũy thấp nhất từ trạng thái ban đầu, phù hợp với bài toán có bước đi mang chi phí khác nhau. Khi áp dụng cho 8-Puzzle, nếu mọi bước đi có cùng chi phí, UCS tương đương BFS nhưng vẫn đảm bảo tính tối ưu trong mọi trường hợp có trọng số khác biệt.

- Iterative Deepening Search (IDS): IDS thực hiện lặp DFS với mức giới hạn độ sâu tăng dần, kết hợp ưu điểm ít bộ nhớ của DFS và khả năng tìm lời giải tối ưu như BFS. Mặc dù có sự trùng lặp trong việc mở rộng các trạng thái đã duyệt ở các độ sâu nhỏ hơn, nhưng tổng hiệu quả về không gian và tính tối ưu khiến IDS phù hợp với các bài toán có không gian lớn mà vẫn cần đảm bảo tìm lời giải ngắn nhất.


## 2.2 Nhóm thuật toán tìm kiếm có thông tin (Informed Search Algorithms)
### Các thành phần chính của bài toán tìm kiếm:
- Trạng thái khởi đầu:
    Lưới 3x3 gồm 8 ô số và 1 ô trống (ký hiệu là 0), với cấu hình ban đầu: [[1, 2, 3], [4, 0, 6], [7, 5, 8]].

- rạng thái đích:
    Lưới được sắp xếp theo thứ tự tăng dần: [[1, 2, 3], [4, 5, 6], [7, 8, 0]].

- Không gian trạng thái:
    Bao gồm tất cả các hoán vị hợp lệ của 9 ô trên lưới 3x3, tức toàn bộ trạng thái có thể đạt được bằng cách di chuyển ô trống.

- Hành động:
    Di chuyển ô trống lên, xuống, trái hoặc phải để đổi vị trí với ô bên cạnh, tạo ra trạng thái mới.

- Chi phí: Mỗi bước di chuyển được tính là 1 đơn vị chi phí.

### Giải pháp:
- Tìm đường đi từ trạng thái ban đầu đến trạng thái đích bằng các thuật toán tìm kiếm có sử dụng hàm heuristic như Greedy Search, A*, và IDA*.

### Hình ảnh gif của từng thuật toán:

### Greedy Search

![Image](https://github.com/user-attachments/assets/7537d6b9-2dee-4cbf-9c44-599650a376f4)

### A*

![Image](https://github.com/user-attachments/assets/f5a9bf1e-d8a1-40b5-bc49-e7df23517564)

### IDA*

![Image](https://github.com/user-attachments/assets/96ba9b4f-2dca-46df-83ac-f7a6061a27db)

### Đánh giá các thuật toán:
- Greedy Search: Mở rộng các trạng thái có giá trị heuristic nhỏ nhất (h(n)), giúp giải nhanh và giảm số trạng thái phải duyệt. Tuy nhiên, do bỏ qua chi phí đi qua (g(n)), thuật toán dễ chọn sai đường, bị kẹt tại cực trị cục bộ.

- A*: Kết hợp chi phí đi qua (g(n)) và ước lượng đến đích (h(n)) để đảm bảo tìm được lời giải tối ưu nếu heuristic chính xác. Dù hiệu quả cao, A* đòi hỏi bộ nhớ lớn do phải lưu và sắp xếp nhiều trạng thái trong hàng đợi ưu tiên.

- IDA*:Mô phỏng A* với mức giới hạn f(n) tăng dần qua từng vòng lặp, giúp tiết kiệm bộ nhớ như DFS. Thích hợp với môi trường giới hạn tài nguyên, nhưng có thể phải duyệt lặp lại nhiều trạng thái, gây tốn thời gian hơn A*.

## 2.3 Nhóm thuật toán tìm kiếm cục bộ (Local Optimization Algorithms)
### Các thành phần chính của bài toán tìm kiếm:
- Trạng thái ban đầu: Lưới 3x3 với các ô số từ 1–8 và ô trống (0), bắt đầu tại: [[0, 1, 3], [4, 2, 5], [7, 8, 6]].

- Trạng thái mục tiêu: Đích đến là [[1, 2, 3], [4, 5, 6], [7, 8, 0]].

- Không gian trạng thái: Gồm tất cả các cách sắp xếp hợp lệ của 9 ô trong lưới.

- Hành động: Di chuyển ô trống (0) theo 4 hướng để đổi chỗ với ô bên cạnh.

- Chi phí: Mỗi bước di chuyển tốn 1 đơn vị chi phí.

### Giải pháp:
- Sử dụng các thuật toán tìm kiếm cục bộ như: Simple Hill Climbing, Steepest Hill Climbing, Random Hill Climbing, Simulated Annealing, Beam Search, Genetic Algorithm.

### Hình ảnh gif của từng thuật toán:

### Simple Hill Climbing

![Image](https://github.com/user-attachments/assets/c019dc9c-b7f5-48fe-ac60-23331579b835)

### Steepest Hill Climbing

![Image](https://github.com/user-attachments/assets/8f211945-67a8-4926-accc-719ca55ed356)

### Random Hill Climbing

![Image](https://github.com/user-attachments/assets/b52ed894-fc5a-4a05-a2de-09c140a0bdd1)

### Simulated Annealing

![Image](https://github.com/user-attachments/assets/0354086f-83bc-46ed-9648-c5e57d49de73)

### Beam Search

![Image](https://github.com/user-attachments/assets/58e1af51-8e8e-413f-93ee-03b7c9738bd9)

### Genetic Algorithm

![Image](https://github.com/user-attachments/assets/f46b83b3-247b-4f7b-a9b4-87f58493e4b5)

### Đánh giá các thuật toán:

- Simple Hill Climbing: Nhanh, đơn giản, chọn trạng thái tốt đầu tiên. Dễ mắc kẹt tại cực trị cục bộ.

- Steepest Hill Climbing: Xét toàn bộ hàng xóm, chọn tốt nhất. Tốt hơn SHC nhưng tốn thời gian hơn.

- Random Hill Climbing: Chọn ngẫu nhiên trong các trạng thái tốt hơn. Trung bình về tốc độ và khả năng tránh kẹt cục bộ.

- Simulated Annealing: Cho phép chọn trạng thái xấu hơn theo xác suất giảm dần. Khám phá tốt nhưng chậm.

- Beam Search: Chỉ giữ số lượng trạng thái tốt nhất giới hạn (beam width). Ổn định, hiệu quả ở mức vừa phải.

- Genetic Algorithm: Mô phỏng tiến hóa: lai – đột biến – chọn lọc. Khả năng tìm lời giải toàn cục cao, nhưng chậm và tốn tài nguyên.

## 2.4 Nhóm thuật toán tìm kiếm trong môi trường phức tạp (Search in complex environments)
### Các thành phần chính của bài toán tìm kiếm:
- Trạng thái ban đầu: 
    - AND-OR Search: Bắt đầu từ một cấu hình cụ thể 3x3 chứa các số 1–8 và ô trống (ví dụ: [[1, 0, 3], [4, 2, 5], [7, 8, 6]]).

    - Belief State Search: Khởi đầu bằng một tập hợp trạng thái có thể xảy ra (belief states), được tạo bằng cách hoán đổi ô trống theo luật di chuyển.

    - Partial Observable Search (POS): Tập belief states ban đầu được xây dựng từ thông tin quan sát giới hạn (ví dụ: biết số 1 ở vị trí (0,0)).

- Trạng thái mục tiêu: [[1, 2, 3], [4, 5, 6], [7, 8, 0]].

- Không gian trạng thái: Tất cả cấu hình hợp lệ của lưới 3x3. Với Belief State và POS, bao gồm cả các tập trạng thái không chắc chắn.

- Hành động: Di chuyển ô trống theo 4 hướng để hoán đổi vị trí với ô liền kề.

- Chi phí: Mỗi lần di chuyển có chi phí là 1.

### Giải pháp:
- Một lời giải là chuỗi hành động từ trạng thái đầu đến trạng thái đích.

- AND-OR Search: Tạo cây tìm kiếm phân nhánh với các nút "AND" và "OR" cho từng trường hợp kết quả không chắc chắn.

- Belief State / POS: Tìm chuỗi hành động áp dụng được cho mọi trạng thái trong belief state ban đầu để đạt đến mục tiêu.

### Hình ảnh gif của từng thuật toán:

### And-Or Search

![Image](https://github.com/user-attachments/assets/09f7a561-542b-4079-876c-5cb4114ae49d)

### Belief State Search

![Image](https://github.com/user-attachments/assets/80db1642-879b-43f3-9491-0a0cc42b3395)

### Partial Observable Search

![Image](https://github.com/user-attachments/assets/b3a0b089-6f0e-415b-92e4-a09ef35f2b7f)

### Đánh giá các thuật toán:
- AND-OR Search: Không dùng heuristic, mỗi hành động có thể dẫn đến nhiều kết quả → cây tìm kiếm rất lớn. Tuy nhiên, chi phí xử lý từng trạng thái thấp, thời gian chạy tổng thể nhanh.

- Belief State Search: Tìm kiếm với tập trạng thái không xác định. Dùng heuristic để chọn 3 trạng thái tốt nhất ở mỗi bước. Không gian bị giới hạn nhưng xử lý mỗi bước tốn kém → thời gian chạy dài.

- Partial Observable Search: Giảm không gian ban đầu nhờ dữ liệu quan sát. Giống BSS nhưng hiệu quả hơn do loại bỏ các trạng thái không phù hợp ngay từ đầu. Tốc độ xử lý tốt hơn BSS, độ chính xác cao hơn.

## 2.5 Nhóm thuật toán tìm kiếm thỏa ràng buộc (Constraint Satisfaction Problem)
### Các thành phần chính của bài toán tìm kiếm:
- Trạng thái ban đầu: Bài toán khởi đầu với một ma trận 3x3 rỗng, trong đó tất cả các ô chưa có giá trị và được biểu diễn bằng None:
[[None, None, None], [None, None, None], [None, None, None]]

- Trạng thái mục tiêu: Mục tiêu là đạt được một cấu hình hoàn chỉnh và hợp lệ, cụ thể là:
[[1, 2, 3], [4, 5, 6], [7, 8, 0]]
Trong đó, số 0 đại diện cho ô trống.

- Không gian trạng thái:
    - Là tập hợp tất cả các cấu hình hợp lệ tạo thành từ hoán vị của các số từ 0 đến 8 trên lưới 3x3, thỏa mãn các ràng buộc sau:
    - Vị trí cố định: Số 1 bắt buộc phải nằm ở ô góc trên bên trái (0,0) như yêu cầu đề bài.
    - Duy nhất: Mỗi giá trị từ 0 đến 8 chỉ xuất hiện đúng một lần trên toàn bộ lưới.

   - Thứ tự hàng ngang: Với bất kỳ ô (i, j) chứa số khác 0, nếu tồn tại ô bên phải (i, j+1) thì giá trị của nó phải bằng grid[i][j] + 1.

    - Thứ tự cột dọc: Tương tự, nếu có ô phía dưới (i+1, j), thì grid[i+1][j] = grid[i][j] + 3.

    - Tính khả giải: Chỉ những cấu hình có tổng số cặp nghịch đảo là số chẵn mới được xem là hợp lệ và có thể giải được.

- Hành động:

    - Backtracking Search: Duyệt từng ô theo thứ tự và thử gán các giá trị có thể. Nếu phát hiện xung đột, thuật toán quay lui (backtrack) để thử giá trị khác. Đây là phương pháp tổng quát nhưng dễ bị rơi vào nhánh sai nếu không có chiến lược định hướng.

    - Forward Checking: Phát triển từ Backtracking, thuật toán này sau mỗi bước gán sẽ loại trừ trước các giá trị không hợp lệ khỏi miền của các ô chưa gán. Điều này giúp phát hiện xung đột sớm và giảm số nhánh sai. Kết hợp thêm hai chiến lược:

        - MRV (Minimum Remaining Values): Ưu tiên ô có ít giá trị hợp lệ nhất.

        - LCV (Least Constraining Value): Chọn giá trị ít ảnh hưởng nhất đến các ô khác.

    - Min-Conflicts Search: Là một thuật toán tìm kiếm cục bộ. Bắt đầu từ một trạng thái hoàn chỉnh (toàn bộ ô đã được gán giá trị ngẫu nhiên), thuật toán xác định các ô đang vi phạm ràng buộc và gán lại giá trị sao cho số xung đột giảm nhiều nhất. Quá trình này được lặp lại cho đến khi đạt trạng thái thỏa mãn hoặc vượt quá giới hạn số bước lặp. Có thể kết hợp với Simulated Annealing để tăng khả năng thoát khỏi cực trị địa phương.

- Chi phí: Vì mục tiêu chỉ là tìm một cấu hình hợp lệ (không tối ưu hóa chi phí), nên mỗi hành động gán hợp lệ đều được coi là có cùng chi phí. Do đó, thông tin chi phí không được dùng làm cơ sở định hướng tìm kiếm như trong các bài toán tối ưu.

### Giải pháp:
- Là một chuỗi các bước gán giá trị hợp lệ từ trạng thái ban đầu (rỗng) cho đến khi đạt được trạng thái mục tiêu hoàn chỉnh.

- Mỗi chiến lược tìm kiếm sẽ tạo ra một chuỗi các trạng thái trung gian khác nhau, nhưng tất cả đều hướng đến duy nhất một trạng thái đích hợp lệ.

- Các thuật toán như Backtracking, Forward Checking và Min-Conflicts thể hiện các cách tiếp cận khác nhau trong giải quyết bài toán ràng buộc – từ duyệt toàn bộ không gian đến tìm kiếm cục bộ có điều chỉnh.

### Hình ảnh gif của từng thuật toán:

### Backtracking Search

![Image](https://github.com/user-attachments/assets/2ee6000e-ba7c-42b3-bc4c-93c67cb683c6)

### Forward Checking

![Image](https://github.com/user-attachments/assets/e66eb06d-9549-4bf6-8653-958f7f4aaa3f)

### Min-Conflicts Search

![Image](https://github.com/user-attachments/assets/f0912dcf-02ed-4e37-8872-20ecaca07b7a)

### Đánh giá các thuật toán:
- Backtracking Search: Phương pháp duyệt theo chiều sâu, gán từng giá trị cho các ô theo thứ tự và kiểm tra tính hợp lệ ngay sau mỗi bước. Nếu phát hiện xung đột, thuật toán sẽ quay lui để thử giá trị khác. Tuy có khả năng liệt kê đầy đủ mọi khả năng, nhưng không hiệu quả với không gian lớn do không có cơ chế loại trừ sớm.

- Forward Checking Search: Giúp loại trừ sớm các giá trị không hợp lệ bằng cách cập nhật miền giá trị còn lại sau mỗi lần gán. Nhờ đó, giảm đáng kể số lượng trạng thái phải duyệt so với Backtracking. Kết hợp chiến lược chọn biến/thứ tự gán giúp tăng hiệu quả trong bài toán có nhiều ràng buộc.

- Min-Conflicts Search: Tìm kiếm cục bộ hiệu quả trong không gian lớn. Bằng cách bắt đầu từ một lời giải đầy đủ nhưng có thể sai, thuật toán điều chỉnh dần bằng cách giảm xung đột qua từng bước. Phù hợp với bài toán không yêu cầu tính toàn vẹn tuyệt đối ngay từ đầu, nhưng cần thời gian tìm nghiệm nhanh.

## 2.6 Nhóm thuật toán học tăng cường (Reinforcement Learning)
### Các thành phần chính của bài toán tìm kiếm:
- Trạng thái ban đầu: Bài toán bắt đầu với một lưới 3x3 chứa các số nguyên từ 1 đến 8 và một ô trống (biểu diễn bằng số 0). Đây là cấu hình khởi đầu của bài toán. Ví dụ: [[0, 1, 3], [4, 2, 5], [7, 8, 6]].

- Trạng thái mục tiêu:
Mục tiêu là đạt được cấu hình đích hợp lệ, nơi các số được sắp xếp theo thứ tự tăng dần từ trái sang phải, từ trên xuống dưới, với ô trống nằm ở góc dưới bên phải: [[1, 2, 3], [4, 5, 6], [7, 8, 0]].

- Không gian trạng thái:
Không gian trạng thái gồm tất cả các cấu hình hợp lệ của lưới 3x3 tạo ra bằng cách hoán đổi các vị trí ô chứa số từ 0 đến 8. Đối với Q-Learning, không gian này không được liệt kê tường minh mà sẽ được khám phá dần trong quá trình học. Thông qua việc trải nghiệm và phản hồi từ môi trường, agent học cách điều hướng trong không gian này mà không cần xây dựng toàn bộ cấu trúc trạng thái trước.

- Hành động:

    - Backtracking Search: Gán lần lượt giá trị cho các ô theo một thứ tự cố định. Nếu phát hiện vi phạm ràng buộc, thuật toán quay lui để thử giá trị khác.

    - Forward Checking: Cải tiến từ Backtracking bằng cách loại bỏ trước các giá trị không hợp lệ trong miền (domain) của các biến chưa gán sau mỗi bước, giúp giảm số lần quay lui.

    - Min-Conflicts Search: Bắt đầu với một trạng thái đầy đủ nhưng có thể không hợp lệ. Ở mỗi bước, chọn một ô gây xung đột và thay đổi giá trị sao cho giảm tổng số vi phạm. Quá trình lặp lại cho đến khi đạt trạng thái hợp lệ hoặc vượt quá số vòng lặp cho phép.

- Chi phí Trong Q-Learning, chi phí được thay thế bằng phần thưởng (reward) để định hướng hành vi:

    - Mỗi bước di chuyển thông thường có phần thưởng âm nhẹ (ví dụ: -1), nhằm thúc đẩy agent tìm đường đi ngắn.

    - Khi đến được trạng thái mục tiêu, agent nhận phần thưởng dương lớn (ví dụ: +100), từ đó học cách tối ưu hành động.

    - Mục tiêu là tối đa hóa tổng phần thưởng tích lũy hơn là tối thiểu số bước.

### Giải pháp:
- Chuỗi các hành động từ trạng thái ban đầu đến trạng thái mục tiêu, được xác định dựa trên chính sách đã học từ bảng Q. Trong quá trình huấn luyện, bảng Q được cập nhật liên tục bằng công thức Bellman, phản ánh giá trị kỳ vọng của từng hành động trong từng trạng thái. Sau khi hội tụ, agent có thể truy xuất đường đi tối ưu bằng cách chọn hành động có giá trị Q cao nhất tại mỗi trạng thái.

### Hình ảnh gif của thuật toán:

### Q-Learning

![Image](https://github.com/user-attachments/assets/b58a8005-de44-43e9-aa58-b245998174ea)

### Đánh giá thuật toán:
- Q-Learning là một thuật toán học tăng cường không cần mô hình (model-free), nơi agent học thông qua thử - sai thay vì dựa vào mô hình môi trường.

- Tại mỗi bước, agent chọn hành động (theo chiến lược Epsilon-Greedy để cân bằng giữa khám phá và khai thác), thực hiện hành động đó, nhận phần thưởng, rồi cập nhật giá trị Q tương ứng.

- Việc xây dựng chính sách tối ưu yêu cầu thời gian huấn luyện dài và cần trải nghiệm nhiều trạng thái để đảm bảo tính tổng quát.

- Dù thời gian học có thể cao và cần nhiều vòng lặp, Q-Learning có ưu điểm lớn ở khả năng thích nghi với môi trường không xác định, đồng thời đảm bảo tìm ra chính sách tốt nếu được huấn luyện đủ lâu.


# 3. Kết luận
- Xây dựng thành công hệ thống mô phỏng bài toán 8-Puzzle

- Triển khai giao diện người dùng trực quan bằng Python và Tkinter, cho phép người dùng tương tác trực tiếp với lưới trò chơi, chọn thuật toán, trạng thái đầu vào và theo dõi quá trình giải.

- Tích hợp đa dạng các thuật toán tìm đường

- Cài đặt và tối ưu các thuật toán cổ điển như BFS, UCS, A*, cũng như các thuật toán hiện đại: Simulated Annealing, Beam Search, Q-Learning, Stochastic Hill Climbing.

- Bổ sung các thuật toán nâng cao như AND-OR Search, Belief State Search, Partial Observable Search với khả năng xử lý môi trường không chắc chắn (uncertainty).

# Tác giả: Lê Hồ Chí Bảo

