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
done    |   (bảng) trang HÓA ĐƠN ĐÃ MUA hiển thị bảng BILL (giống bảng budget)
done    |       +Hiển thị các hóa đơn mua đồ, bán đồ
done    |       +email mua thành công(sẽ hiện các thứ giống bill, hiện thị mã id của bill)
done    |   (bảng) lưu favorite product bằng cách tạo 1 bảng db favorite (id, productId, userId)
            khi query thì sẽ query các favorite có userId == current_user_id
    |   cho người dùng tìm kiếm + follow nhau (sách chap 12)

click vào search ở trang chủ
=> chạy tới hàm search_page(type = 'products', kw)

click vào tab đc hiển thị bằng tab <a> (giống category trang chủ)
=> chạy tới hàm search_page(type = chữ trong tag <a> , kw = kw đang đc truyền vào)

click search ở trang search
=> chạy tới hàm search_page(type = 'products', kw = form.kw.data)


search_page(type,kw):
    form = SearchForm (phải có để trong trang search user có thể dùng để search tiếp kw khác)
    products = Product.query()
    users = User.query()
	return (search.html,
		  type = products/users
		  kw = kw,
          form = form,
          products = products
          users = users
          )


add sp xong trên flash cho phép đi tới trang profile để xem các sp họ vừa post
lúc add budget xong trên flash cho phép đi tới budget history
sửa lại không hiển thị sp của mình ngoài trang chủ và trong product detail
gỡ recaptcha field
sửa lại default budget là 0đ
chưa có hàm fromnow()
lúc resell phải thay đổi lại ngày đăng bán
chú ý mấy cái datetime.now()
hàm ping để xem last seen
ẩn nút POST nếu là guest