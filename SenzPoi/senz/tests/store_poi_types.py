# -*- coding:utf-8 -*-
__author__ = 'wzf'

import json

level1_poi_types = ("美食", "购物", "生活服务", "娱乐休闲",
                 "汽车", "医疗保健", "酒店宾馆", "旅游景点",
                 "文化场馆", "教育学校",  "银行金融", "基础设施", "房产小区")


poi_types = {
    "美食" : {
        "中餐厅" : 'chinese_restaurant',
        "日韩菜" : {
                 "日本料理" : 'japan_korea_restaurant',
                 "韩国料理" : 'japan_korea_restaurant',
        },
        "西餐" : 'western_restaurant',
        "烧烤" : 'bbq',
        "火锅" : 'chafing_dish',
        "海鲜" : 'seafood',
        "素食" : 'vegetarian_diet',
        "清真" : 'muslim',
        "自助餐" : 'buffet',
        "面包甜点" : 'dessert',
        "冷饮店" : 'cooler',
        "小吃快餐" : 'snack_bar',

    },
    "购物" : {
        "综合商场" : 'comprehensive_market',
        "便利店" : 'convenience_store',
        "超市" : 'supermarket',
        "数码家电" : 'digital_store',
        "花鸟鱼虫" : 'pet_market',
        "家具家居建材" : 'furniture_store',
        "农贸市场" : 'farmers_market',
        "小商品市场" : 'commodity_market',
        "旧货市场" : 'flea_market',
        "体育户外" : 'sports_store',
        "服饰鞋包" : 'clothing_store',
        "图书音像" : 'video_store',
        "眼镜店" : 'glass_store',
        "母婴儿童" : 'mother_store',
        "珠宝饰品" : 'jewelry_store',
        "化妆品" :  'cosmetics_store',
        "礼品" : 'gift_store',
        "摄影器材" : 'photography_store',
        "拍卖典当行" : 'pawnshop',
        "古玩字画" : 'antique_store',
        "自行车专卖" : 'bike_store',
        "烟酒专卖" :  'cigarette_store',
        "文化用品" : 'stationer',
    },
    "生活服务" : {
        "旅行社" :  'travel_agency',
        "票务代售" : {
            "飞机票代售" :  'ticket_agent',
            "火车票代售" :  'ticket_agent',
            "汽车票代售" :  'ticket_agent',
            "公交及IC卡" :  'ticket_agent',
        },
        "邮局速递" : {
            "邮局" : 'post_office',
            "速递" : 'post_office',
        },
        "通讯服务" : {
            "中国电信营业厅" : 'telecom_offices',
            "中国网通营业厅" : 'telecom_offices',
            "中国移动营业厅" : 'telecom_offices',
            "中国联通营业厅" : 'telecom_offices',
            "中国铁通营业厅" : 'telecom_offices',
        },
        "报刊亭" :  'newstand',
        "自来水营业厅" : 'water_supply_office',
        "电力营业厅" :  'electricity_office',
        "摄影冲印" : 'photographic_studio',
        "洗衣店" : 'laundry',
        "招聘求职" : 'talent_market',
        "彩票" :  'lottery_station',
        "家政" : {
            "月嫂保姆" :  'housekeeping',
            "保洁钟点工" : 'housekeeping',
            "开锁" : 'housekeeping',
            "送水" : 'housekeeping',
            "家电维修" : 'housekeeping',
            "搬家" : 'housekeeping',
        },
        "中介机构" :  'intermediary',
        "宠物服务" :  'pet_service',
        "废品收购站" :  'salvage_station',
        "福利院养老院" : 'welfare_house',
        "美容美发" : 'barbershop',
    },
    "娱乐休闲" : {
        "洗浴推拿足疗" :  'bath_sauna',
        "KTV" : 'ktv',
        "酒吧" : 'bar',
        "咖啡厅" : 'coffee',
        "夜总会" : 'night_club',
        "电影院" : 'cinema',
        "剧场音乐厅" : 'odeum',
        "度假疗养" : 'resort',
        "户外活动" : {
            "游乐场": 'outdoor',
            "垂钓园" : 'outdoor',
            "采摘园" : 'outdoor',
        },
        "游戏棋牌" : {
            "游戏厅" :  'game_room',
            "棋牌室" :  'game_room',
        },
        "网吧" : 'internet_bar',
    },
    "汽车" : {
        "加油站" : {
            "中石化" : 'gas_station',
            "中石油" : 'gas_station',
            "其它加油加气站" : 'gas_station',
        },
        "停车场" : 'parking_plot',
        "汽车销售" :  'auto_sale',
        "汽车维修" :  'auto_repair',
        "摩托车" : {
            "摩托车服务相关" : 'motorcycle',
            "销售" : 'motorcycle',
            "维修" : 'motorcycle',
            "其它摩托车" : 'motorcycle',
        },
        "汽车养护" : 'car_maintenance',
        "洗车场" : 'car_wash',
    },
    "医疗保健" : {
        "综合医院" : 'hospital',
        "诊所" : 'clinic',
        "急救中心" : 'emergency_center',
        "药房药店" :  'drugstore',
    },
    "酒店宾馆" : {
        "酒店宾馆" :  'motel',
        "星级酒店" : 'hotel',
        "经济型酒店" : 'economy_hotel',
        "旅馆招待所" :  'guest_house',
        "青年旅社" : 'hostel',
    },
    "旅游景点" : 'scenic_spot',
    "文化场馆" : {
        "博物馆" : 'museum',
        "展览馆" : 'exhibition_hall',
        "科技馆" : 'science_museum',
        "图书馆" : 'library',
        "美术馆" : 'gallery',
        "会展中心" : 'convention_center',
    },
    "教育学校" : {
        "大学" :  'university',
        "中学" :  'high_school',
        "小学" : 'primary_school',
        "幼儿园" : 'kinder_garten',
        "培训" :  'training_institutions',
        "职业技术学校" : 'technical_school',
        "成人教育" :  'adult_education',
    },
    "银行金融" : {
        "银行" : 'bank',
        "自动提款机" :  'atm',
        "保险公司" : 'insurance_company',
        "证券公司" :  'security_company',
    },
    "基础设施" : {


        "交通设施" : {
            "公交车站" : 'traffic',
            "地铁站" : 'traffic',
            "火车站" : 'traffic',
            "长途汽车站" : 'traffic',
            "公交线路" : 'traffic',
            "地铁线路" : 'traffic',
        },
        "公共设施" : {
            "公共厕所" : 'public_utilities',
            "公用电话" : 'public_utilities',
            "紧急避难场所" : 'public_utilities',
        },
        "道路附属" : {
            "收费站" : 'toll_station',
            "服务区" : 'toll_station',
        },
        "其它基础设施" : 'other_infrastructure',
    },
    "房产小区" : {


        "住宅区" : {
            "住宅小区" : 'residence',
            "别墅" : 'residence',
            "宿舍" : 'residence',
            "社区中心" : 'residence',
        },
        "商务楼宇" : 'business_building',
    },
}

location_level1_type = ('dining', 'shopping', 'life_service', 'entertainment', 'auto_related', 'healthcare', 'hotel', 'scenic_spot', 'exhibition', 'education', 'finance', 'infrastructure', 'estate')

mapping_types = {
    'dining' : {
        'chinese_restaurant', 'japan_korea_restaurant', 'western_restaurant', 'bbq', 'chafing_dish', 'seafood', 'vegetarian_diet', 'muslim', 'buffet', 'dessert', 'cooler', 'snack_bar',
    },
    'shopping' : {
        'comprehensive_market', 'convenience_store', 'supermarket', 'digital_store', 'pet_market', 'furniture_store', 'farmers_market', 'commodity_market', 'flea_market', 'sports_store', 'clothing_store', 'video_store', 'glass_store', 'mother_store', 'jewelry_store', 'cosmetics_store', 'gift_store', 'photography_store', 'pawnshop', 'antique_store', 'bike_store', 'cigarette_store', 'stationer',
    },
    'life_service' : {
        'travel_agency', 'ticket_agent', 'post_office', 'telecom_offices', 'newstand', 'water_supply_office', 'electricity_office', 'photographic_studio', 'laundry', 'talent_market', 'lottery_station', 'housekeeping', 'intermediary', 'pet_service', 'salvage_station', 'welfare_house', 'barbershop',
    },
    'entertainment' : {
        'bath_sauna', 'ktv', 'bar', 'coffee', 'night_club', 'cinema', 'odeum', 'resort', 'outdoor', 'game_room', 'internet_bar',
    },
    'auto_related' : {
        'gas_station', 'parking_plot', 'auto_sale', 'auto_repair', 'motorcycle', 'car_maintenance', 'car_wash',
    },
    'healthcare' : {
        'hospital', 'clinic', 'emergency_center', 'drugstore',
    },
    'hotel' : {
        'motel', 'hotel', 'economy_hotel', 'guest_house', 'hostel',
    },
    'scenic_spot' : {
    },
    'exhibition' : {
        'museum', 'exhibition_hall', 'science_museum', 'library', 'gallery', 'convention_center',
    },
    'education' : {
        'university', 'high_school', 'primary_school', 'kinder_garten', 'training_institutions', 'technical_school', 'adult_education',
    },
    'finance' : {
        'bank', 'atm', 'insurance_company', 'security_company',
    },
    'infrastructure' : {
        'traffic', 'public_utilities', 'toll_station', 'other_infrastructure',
    },
    'estate' : {
        'residence', 'business_building'
    },
}

from base import TestBase

POI_SOURCE = 'tencent'

def format_types(origin, res, poi_source, up=''):
    for t in origin:
        type_now = t if not up else up + ';' + t
        if isinstance(origin[t], dict):
            format_types(origin[t], res, poi_source, type_now)
        elif isinstance(origin[t], str):
            res.append(dict(source=poi_source, mapping_type=origin[t], origin_type=type_now))

class StorePoiTypes(TestBase):
    def __init__(self):
        super(StorePoiTypes, self).__init__()
        self.headers = {"Content-type":"application/json"}

    def store(self):
        res = []
        format_types(poi_types, res, POI_SOURCE)
        #print json.dumps(res, encoding='utf-8', ensure_ascii=False)

        print len(res)

        response = self.avos_manager.saveData('poi_types', res)

        print response


if __name__ == '__main__':
    testor = StorePoiTypes()
    testor.store()