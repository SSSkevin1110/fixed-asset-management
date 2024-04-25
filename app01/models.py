from django.db import models
from django.forms import forms


class Department(models.Model):
    """部门信息"""
    Name = models.CharField(max_length=16, blank=False, verbose_name='部门名', unique=True)

    def __str__(self):
        return self.Name

class RatioInfo(models.Model):
    """预计净残值率"""
    Type = models.CharField(verbose_name="设备类型", max_length=64)
    Ratio = models.DecimalField(verbose_name="预计净残值率", max_digits=5, decimal_places=2)

    def __str__(self):
        return self.Type


class AdminInfo(models.Model):
    """用户信息"""
    Username = models.CharField(max_length=32, verbose_name='用户名')
    Password = models.CharField(max_length=64, verbose_name='密码')
    BelongTo = models.ForeignKey(verbose_name='所属部门', to='Department', to_field='id', on_delete=models.CASCADE)
    user_type_choices = (
        (1, "管理员"),
        (2, "普通用户")
    )
    user_type = models.IntegerField(verbose_name="用户类型", choices=user_type_choices, default=2)

class AssetsInfo(models.Model):
    """资产信息"""
    Registration_number = models.CharField(max_length=64, verbose_name='登记编号', unique=True)
    Model = models.CharField(max_length=16, verbose_name='设备型号', blank=False)
    Name = models.CharField(max_length=16, verbose_name='设备名称', blank=False)
    Supplier_info = models.ForeignKey(verbose_name='供应商信息', to='Supplier', to_field='id', on_delete=models.CASCADE)
    Unit_price = models.DecimalField(verbose_name="单价", decimal_places=3, max_digits=15)
    Applicant = models.CharField(max_length=32, verbose_name='登记人', blank=False)
    BelongTo = models.ForeignKey(verbose_name='所属部门', to='Department', to_field='id', on_delete=models.CASCADE)
    asset_type = models.ForeignKey('RatioInfo', to_field='id', verbose_name="资产类型", on_delete=models.CASCADE,
                                   default=1)
    now_type = models.IntegerField(choices=((1, '已确认'), (0, '未确认')), default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False, verbose_name='已确认状态')  # 添加这行代码

    def __str__(self):
        return self.Registration_number


class AssetDamageInfo(models.Model):
    """资产报废字段和关联关系"""
    Time = models.DateField(verbose_name='申请时间')
    Reg_number = models.ForeignKey('AssetsInfo', to_field='Registration_number', verbose_name='登记编号', max_length=64,
                                   on_delete=models.CASCADE)
    Model = models.CharField(verbose_name='设备型号', max_length=16)
    Name = models.CharField(verbose_name='设备名称', max_length=16)
    Price = models.DecimalField(verbose_name="购入单价", decimal_places=3, max_digits=15)
    LiftYears = models.DecimalField(verbose_name='使用年限', decimal_places=3, max_digits=10)
    Type = models.ForeignKey('RatioInfo', to_field='id', verbose_name="资产类型", on_delete=models.CASCADE)
    Depreciation_price = models.DecimalField(verbose_name="折旧价格", decimal_places=3, max_digits=15)
    now_type = models.IntegerField(choices=((1, '已确认'), (0, '未确认')), default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False, verbose_name='已确认状态')  # 添加这行代码



class AssetChangeInfo(models.Model):
    """资产转让字段和关联关系"""
    Time = models.DateField(verbose_name='申请时间')
    Reg_number = models.ForeignKey('AssetsInfo', to_field='Registration_number', verbose_name='登记编号', max_length=64,
                                   on_delete=models.CASCADE)
    Model = models.CharField(verbose_name='设备型号', max_length=16)
    Name = models.CharField(verbose_name='设备名称', max_length=16)
    OriginalUnit = models.ForeignKey('Department', related_name='asset_change_original_unit',
                                     max_length=16, verbose_name='原使用单位', on_delete=models.CASCADE)
    NowUnit = models.ForeignKey('Department', related_name='asset_change_now_unit',
                                     max_length=16, verbose_name='现使用单位', on_delete=models.CASCADE)
    # NowUnit = models.CharField(max_length=16, verbose_name='现使用单位', blank=False)
    Applicant = models.CharField(max_length=32, verbose_name='申请人', blank=False)
    now_type = models.IntegerField(choices=((1, '已确认'), (0, '未确认')), default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False, verbose_name='已确认状态')  # 添加这行代码


class AssetMaintainInfo(models.Model):
    """资产维修字段和关联关系"""
    Time = models.DateField(verbose_name='申请时间')
    # Reg_number = models.CharField(verbose_name='登记编号', max_length=64)
    Reg_number = models.ForeignKey('AssetsInfo', to_field='Registration_number', verbose_name='登记编号', max_length=64,
                                   on_delete=models.CASCADE)
    Model = models.CharField(verbose_name='设备型号', max_length=16)
    Name = models.CharField(verbose_name='设备名称', max_length=16)
    BelongTo = models.ForeignKey(verbose_name='申请部门', to='Department', to_field='id', on_delete=models.CASCADE)
    Applicant = models.CharField(max_length=32, verbose_name='申请人', blank=False)
    now_type = models.IntegerField(choices=((1, '已确认'), (0, '未确认')), default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False, verbose_name='已确认状态')  # 添加这行代码


class Supplier(models.Model):
    """供应商"""
    Name = models.CharField(verbose_name='供应商名称', max_length=32)
    Supplier_address = models.CharField(max_length=64, verbose_name="供应商地址")
    Phone = models.CharField(verbose_name='供应商电话', max_length=32)

    def __str__(self):
        return f"{self.Name} ： {self.Supplier_address}"


