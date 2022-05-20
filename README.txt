App chợHơiTốt.com (đồ án cuối kì môn SOA)
Thành viên nhóm 8:
    + Phạm Hải Đăng  519H0277
    + Dương Chí Kiện 519H0077

done    |   đăng nhập, đăng kí (có xác thực email, resend confirm email)
done    |   ghi nhớ đăng nhập
done    |   forgot password
done    |   injection year now ở dưới footer
done    |   reCAPTCHA trong login
done    |   profile user(chỉnh sửa profile)+ hiển thị tin đang bán + có avatar sd Gravatar :
done    |       + change password sau khi đăng nhập
done    |       + Edit profile (username, full name, phone, bio)
done    |       + Có avatar (avatar sẽ dựa trên cột điểm của user, mỗi lần mua hàng sẽ đc cộng điểm)
done    |   (budget là Đồng, cho người dùng tự nạp) (VERIFY BẰNG OTP CODE )
done    |   Xem lịch sử biến động số dư
done    |   up sản phẩm+post của mình lên có chia category (giống chợ tốt)
done    |   Khi bấm vô trang chi tiết sp:
done    |   	+Nút mua (xác thực email)
done    |   	+Xem người bán last seen
done    |   	+Nút xem profile người bán
done    |   	+Hiển thị các sp khác lquan cùng cate ở dưới
done    |   mua sản phẩm 
done    |   xem tất cả tin của mình đang bán trong trang profile
done    |       +liệt kê các sp ĐANG đc đăng bán
done    |       +thay vì nút mua thì sẽ là nút update, delete (khi ở trang người khác thì sẽ là nút mua)
done    |   làm trang đã mua
done    |       +liệt kê các sp đã đc mua thành công
done    |       +có option cho phép bán lên lại ==> set status của product lại thành 'selling'
done    |   (bảng) trang HÓA ĐƠN ĐÃ MUA hiển thị bảng BILL (giống bảng budget)
done    |       +Hiển thị các hóa đơn mua đồ, bán đồ
done    |       +email mua thành công(sẽ hiện các thứ giống bill, hiện thị mã id của bill)
done    |   (bảng) lưu favorite product bằng cách tạo 1 bảng db favorite (id, productId, userId)
            khi query thì sẽ query các favorite có userId == current_user_id
done    |   cho người dùng tìm kiếm : sản phẩm / user khác 

    |   follow nhau (sách chap 12)

######## NOTE ########

done    sửa lại default budget là 0đ
done    lúc resell phải thay đổi lại ngày đăng bán
done    chú ý mấy cái datetime.now()
done    link nạp tiền đã nạp r vẫn xài lại đc?
done    ẩn nút POST với guest
done    gỡ recaptcha field
done    chưa có hàm fromnow()
done    hàm để cập nhật last seen
done    Gửi mail nạp tiền thành công bạn đã gửi
done    Sort product theo thời gian
done    sort sản phẩm (trang đang bán, trang chủ và trang kết quả search):
            +theo date (mặc định)
            +theo giá (tăng giảm)
            +theo alphabet (tăng giảm)
hàm resend otp trong màn NHẬP OTP
chỉnh lại vị trí nút search ở trang chủ









bảng user:
    thêm cột status để xem có đang có 1 GD NẠP TIỀN chưa thực hiện xong kh (giống gki)
    TRUE LÀ CÓ THỂ NẠP và ngược lại
    thêm cột last_add_budget (default = None)

khi mà bấm 'NẠP' trong trang REQUEST NẠP:
    +Check user.last_add_budget:
    ==> if user.last_add_budget != None (vì lúc mới tạo tk thì default là None)
    ==> nếu now() - user.last_add_budget >= 3 phút
    ==> set 'user_status' = TRUE
    +Nếu 'user_status' == TRUE thì tiến hành request nạp tiền
    ==> set 'user_status' thành FALSE ==> Tức là tạm thời không thể nạp tiếp
    ==> lưu biến user.last_add_budget thành now()
    ==> tạo ra 1 row OTP
    ==> Gửi OTP.OTP_CODE đến current_user.user_email
    ==> direct đến trang NHẬP OTP
    +Nếu 'user_status' == FALSE
    ==> direct đến trang NHẬP OTP
    ==> flash (đang có gd khác)
    ==> gửi lại otp khác ???


khi bấm vô 'XÁC NHẬN' ở trang NHẬP OTP:
    +query ra OTP ROW có:
        OTP_CODE ĐC ĐIỀN 
        STATUS = 'PENDING' 
        user_id==current_user.id 
        ==> .LAST() vì đó chắc chắn là otp cuối cùng đc tạo 
        query ra otp thi cu lay last vi khi bam request thi trong vong 3 phut tiep theo se chi co 1 otp là dùng để xác thực
    +Nếu now() - timestamp >= 3 phút
        ==> flash(OTP đã quá hạn, vui lòng gửi request add budget khác)
    +Nếu now() - timestamp <= 3 phút
        ==> hợp lệ
        ==> add vô budget
        ==> set user.status = TRUE
        ==> set otp.status = EXPIRED
    +Nếu không ra: flash (OTP không đúng)


bảng otp:
    id:
    status: default 'PENDING'   // khi mà mới tạo sẽ là 'PENDING'
                                // khi mà verify otp thành công => nạp thành công => thì set thành 'USED'
                                // khi mà verify otp 
    otp_code = random 6 số (nếu trong BẢNG OTP có row nào status là PENDING mà OTP_CODE trùng thì random 6 số khác)
    timestamp:
    user_id: fk ==> current_user.id
