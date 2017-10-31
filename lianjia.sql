create table `lj_xiaoqu` ( 
`id` int(10) unsigned NOT NULL AUTO_INCREMENT, 
`xiaoqu_id` bigint(14) unsigned NOT NULL, 
`xiaoqu_name` varchar(64) NOT NULL, 
`avg_price` int(6) unsigned NOT NULL, 
`bulit_year` int(4) unsigned NOT NULL,  
`county` varchar(20) NOT NULL, 
`district` varchar(20) NOT NULL, 
`current_sale` int(3) unsigned NOT NULL, 
`thirtydays_deal` int(3) unsigned NOT NULL,
PRIMARY KEY (`id`)) ENGINE=innodb AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

create table`lj_xiaoqu_page_url` (
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`xiaoqu_page_url` varchar(255) NOT NULL,
PRIMARY KEY (`id`)) ENGINE=innodb AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

create table`lj_good_fang_url` (
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`fang_id` bigint(14) unsigned NOT NULL, 
`good_fang_url` varchar(255) NOT NULL,
PRIMARY KEY (`id`)) ENGINE=innodb AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

insert into lj_xiaoqu values( NULL, 
'1111027382209',
'远洋山水', 
'72460', 
'2005', 
'石景山', 
'鲁谷', 
'67', 
'26', 
'http://bj.lianjia.com/xiaoqu/1111027382209/');


insert into lj_xiaoqu_page_url values(NULL,
'http://bj.lianjia.com/xiaoqu/xicheng/pg2/')

insert into lj_good_fang_url values(NULL, 123,'http://bj.lianjia.com/ershoufang/101101087856.html')
