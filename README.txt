App chợHơiTốt.com (đồ án cuối kì môn SOA)
Thành viên nhóm 8:
    + Phạm Hải Đăng  519H0277
    + Dương Chí Kiện 519H0077

done    |   đăng nhập, đăng kí (có xác thực email, resend confirm email)
done    |   ghi nhớ đăng nhập
done    |   forgot password
done    |   injection year now ở dưới footer
done    |   change password sau khi đăng nhập
done    |   reCAPTCHA trong login
    |   profile user(chỉnh sửa profile)+ hiển thị tin đang bán + có avatar sd Gravatar
    |   up sản phẩm+post của mình lên có chia category (giống chợ tốt)
    |   mua sản phẩm (budget là Đồng Tốt, cho người dùng tự nạp) (have verify email to confirm )
    |   quản lí tin (xem tất cả tin của mình gồm đang bán và đã bán)
    |   cho người dùng tìm kiếm + follow nhau (sách chap 12)
    |   Khi bấm vô trang chi tiết sp:
    |   	+Xem người bán last seen
    |   	+Nút mua (xác thực email)
    |   	+Nút xem profile người bán
    |   	+Hiển thị các sp khác lquan cùng cate ở dưới
    |   (bảng) notify khi có người khác mua của mình, khi mình bán thành công, đăng tin thành công???
        trong bảng notify có column 'seen', mặc định khi tạo sẽ bằng False
        mỗi lần load trang chủ sẽ kiểm tra có noti có seen bằng False, nếu có thì sẽ cho biến have_noti = True
        rồi truyền vào template, trong template sẽ check biến nếu có thì sẽ có chấm ở icon noti
        khi bấm vô trang tb, sẽ set tất cả noti 'seen' về True
    |   (bảng) lưu favorite product bằng cách tạo 1 bảng db favorite (id, productId, userId)
        khi query thì sẽ query các favorite có userId == current_user_id
    |   (bảng) trả giá, mua lại: tạo ra 1 bảng 
     