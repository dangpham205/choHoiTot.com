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
done    |   (budget là Đồng hoi Tốt, cho người dùng tự nạp) (have verify email to confirm )
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
        |   (bảng) trang HÓA ĐƠN ĐÃ MUA hiển thị bảng BILL (giống bảng budget)
        |       +Hiển thị các hóa đơn mua đồ, bán đồ
done    |       +email mua thành công(sẽ hiện các thứ giống bill, hiện thị mã id của bill)
    |   (bảng) lưu favorite product bằng cách tạo 1 bảng db favorite (id, productId, userId)
        khi query thì sẽ query các favorite có userId == current_user_id
    |   cho người dùng tìm kiếm + follow nhau (sách chap 12)

bill:
    id: mã gd
    type: ĐƠN BÁN HÀNG / ĐƠN MUA HÀNG
    date: ngày tạo bill
    product_name : sản phẩm đc gd (phải lưu lại vì giá sp sau này có thể bị ng mua lại đổi) 
    total: giá sp lúc đó gd (phải lưu lại vì giá sp sau này có thể bị ng mua lại đổi)
    person_id: lưu lại id của ng mua/bán
    owner_id (fk)

mỗi lần có gd mua thành công: lưu bill cho cả seller và buyer

query trang bill:
    nếu owner_id trùng:
        + title: type
        + ngày tạo bill: date
        + hiện tt sp (name, giá)
        + tên ng mua
        + nếu type là ĐƠN BÁN  thì hiện "người mua: person_id"
          nếu type là ĐƠN MUA  thì hiện "người bán: person_id"


add sp xong trên flash cho phép đi tới trang profile để xem các sp họ vừa post
lúc add budget xong trên flash cho phép đi tới budget history
sửa lại không hiển thị sp của mình ngoài trang chủ và trong product detail
gỡ recaptcha field
sửa lại default budget là 0đ
chưa có hàm fromnow()
footer
xóa unique trong model user.user_name
trong email xác nhận mua hiển thị thêm id của bill (mã đơn hàng ), ngày tạo bill
lúc resell phải thay đổi lại ngày đăng bán