App chợHơiTốt.com (đồ án cuối kì môn SOA)
Thành viên nhóm 8:
    + Phạm Hải Đăng  519H0277
    + Dương Chí Kiện 519H0077

done    |   đăng nhập, đăng kí (có xác thực email, resend confirm email)
done    |   ghi nhớ đăng nhập
done    |   forgot password
done    |   injection year now ở dưới footer
done    |   reCAPTCHA trong login
        |   profile user(chỉnh sửa profile)+ hiển thị tin đang bán + có avatar sd Gravatar :
done                + change password sau khi đăng nhập
done                + Edit profile (username, full name, phone, bio)
done                + Có avatar (avatar sẽ dựa trên cột điểm của user, mỗi lần mua hàng sẽ đc cộng điểm)
done    |   (budget là Đồng hoi Tốt, cho người dùng tự nạp) (have verify email to confirm )
done    |   Xem lịch sử biến động số dư
done    |   up sản phẩm+post của mình lên có chia category (giống chợ tốt)
        |   Khi bấm vô trang chi tiết sp:
done    |   	+Nút mua (xác thực email)
done    |   	+Xem người bán last seen
done    |   	+Nút xem profile người bán
done    |   	+Hiển thị các sp khác lquan cùng cate ở dưới
done    |   mua sản phẩm 
    |    xem tất cả tin của mình đang bán trong trang profile
    |        +liệt kê các sp ĐANG đc đăng bán
	|        +thay vì nút mua thì sẽ là nút update, delete
    |    làm trang đã mua
    |        +liệt kê các sp đã đc mua thành công
    |        +có option cho phép bán lên lại ==> set status của product lại thành 'selling'
    |   (bảng) trang HÓA ĐƠN ĐÃ MUA hiển thị bảng BILL (giống bảng budget)
    |        +email mua thành công(sẽ hiện các thứ giống bill)
    |   (bảng) notify khi có người khác mua của mình, khi mình bán thành công, đăng tin thành công???
        trong bảng notify có column 'seen', mặc định khi tạo sẽ bằng False
        mỗi lần load trang chủ sẽ kiểm tra có noti có seen bằng False, nếu có thì sẽ cho biến have_noti = True
        rồi truyền vào template, trong template sẽ check biến nếu có thì sẽ có chấm ở icon noti
        khi bấm vô trang tb, sẽ set tất cả noti 'seen' về True
    |   (bảng) lưu favorite product bằng cách tạo 1 bảng db favorite (id, productId, userId)
        khi query thì sẽ query các favorite có userId == current_user_id
    |   cho người dùng tìm kiếm + follow nhau (sách chap 12)
     

add sp xong trên flash cho phép đi tới trang profile để xem các sp họ vừa post
lúc add budget xong trên flash cho phép đi tới budget history
sửa lại không hiển thị sp của mình ngoài trang chủ và trong product detail
gỡ recaptcha field
sửa lại default budget là 0đ
chưa có hàm fromnow()
footer