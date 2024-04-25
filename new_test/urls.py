"""
URL configuration for new_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from app01.views import login, admin, department, supplier, asset, ratio, maintain, damage, change, user

urlpatterns = [
    # 　登陆
    path('', login.index),
    path('login/', login.login_view),
    path('logout/', login.logout),
    # 图片验证码
    path('image/code/', login.image_code),

    # 管理员界面
    path('admin/', admin.admin_info),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/del/', admin.admin_del),
    path('admin/<int:nid>/reset/', admin.admin_reset),
    path('admin/<int:nid>/edit/', admin.admin_edit),

    # 　部门表
    path('dept/', department.dept),
    path('dept/add/', department.dept_add),
    path('dept/del/', department.dept_del),
    path('dept/<int:nid>/edit/', department.dept_edit),

    #  供应商信息列表
    path('supplier/', supplier.supplier),
    path('supplier/add', supplier.supplier_add),
    path('supplier/<int:nid>/edit', supplier.supplier_edit),
    path('supplier/<int:nid>/del', supplier.supplier_del),

    #  资产表
    path('asset/', asset.asset),
    path('asset/add/', asset.asset_add),
    path('asset/<int:nid>/edit', asset.asset_edit),
    path('asset/<int:nid>/del/', asset.asset_del),
    path('asset/<int:nid>/maintain/add/', asset.asset_maintain),
    path('asset/<int:nid>/damage/add/', asset.asset_damage),
    path('asset/<int:nid>/change/add/', asset.asset_change),
    #  确认功能
    path('asset/info/verify/<str:Registration_number>/', asset.info_verify),

    #  预计净残值率参考
    path('ratio/', ratio.ratio),
    path('ratio/add/', ratio.ratio_add),
    path('ratio/<int:nid>/edit', ratio.ratio_edit),
    path('ratio/<int:nid>/del', ratio.ratio_del),

    # ********** 资产维修  **********
    path('asset/maintain/', maintain.asset_maintain_list),
    #  本功能同时写入到asset内
    path('asset/maintain/add/', maintain.asset_maintain_add),
    # 删除
    path('asset/maintain/<int:nid>/del/', maintain.asset_maintain_del),
    # 确认功能
    path('asset/maintain/info/verify/<int:Reg_number>/', maintain.info_verify),

    # **********  资产报废  **********
    path('asset/damage/', damage.asset_damage_list),
    path('asset/damage/<int:nid>/del/', damage.asset_damage_del),
    # 确认功能
    path('asset/damage/info/verify/<int:Reg_number>/', damage.info_verify),

    # **********  资产转让  **********
    path('asset/change/', change.asset_change_list),
    path('asset/change/add/', change.asset_change_add),
    # 删除
    path('asset/change/<int:nid>/del/', change.asset_change_del),
    # 确认功能
    path('asset/change/info/verify/<int:Reg_number>/', change.info_verify),

    #  user
    path('user/', user.user_asset),
    # path('asset/add_u/', user.asset_add),





]
