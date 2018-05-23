DROP DATABASE IF EXISTS `news_spider`;
CREATE DATABASE `news_spider` /*!40100 DEFAULT CHARACTER SET utf8 */;


use news_spider;


CREATE TABLE `channel` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(20) COMMENT '频道编号',
  `name` VARCHAR(20) COMMENT '频道名称',
  `description` VARCHAR(500) DEFAULT '' COMMENT '描述',
  `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY idx_code (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='频道表';


CREATE TABLE `fetch_task` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `platform_id` TINYINT DEFAULT 0 COMMENT '平台id（1:微信;2:微博;3:头条）',
  `channel_id` TINYINT DEFAULT 0 COMMENT '频道id',
  `follow_id` VARCHAR(45) DEFAULT '' COMMENT '关注账号id',
  `follow_name` VARCHAR(45) DEFAULT '' COMMENT '关注账号名称',
  `avatar_url` VARCHAR(512) DEFAULT '' COMMENT '关注账号头像',
  `fetch_url` VARCHAR(512) DEFAULT '' COMMENT '抓取入口',
  `flag_enabled` TINYINT DEFAULT 0 COMMENT '启用标记（0:未启用;1:已启用）',
  `description` VARCHAR(500) DEFAULT '' COMMENT '描述',
  `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY idx_platform_follow_id (`platform_id`, `follow_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='抓取任务表';


CREATE TABLE `fetch_result` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `task_id` INT NOT NULL COMMENT '任务id',
  `platform_id` TINYINT DEFAULT 0 COMMENT '平台id（1:微信;2:微博;3:头条）',
  `platform_name` VARCHAR(50) DEFAULT '' COMMENT '平台名称（1:微信;2:微博;3:头条）',
  `channel_id` TINYINT DEFAULT 0 COMMENT '频道id',
  `channel_name` VARCHAR(50) DEFAULT '' COMMENT '频道名称',
  `article_id` VARCHAR(50) DEFAULT '' COMMENT '文章id',
  `article_url` VARCHAR(512) DEFAULT '' COMMENT '文章链接',
  `article_title` VARCHAR(100) DEFAULT '' COMMENT '文章标题',
  `article_author_id` VARCHAR(100) DEFAULT '' COMMENT '文章作者id（对应follow_id）',
  `article_author_name` VARCHAR(100) DEFAULT '' COMMENT '文章作者名称（对应follow_name）',
  `article_tags` VARCHAR(100) DEFAULT '' COMMENT '文章标签（半角逗号分隔）',
  `article_abstract` VARCHAR(500) DEFAULT '' COMMENT '文章摘要',
  `article_content` MEDIUMTEXT COMMENT '文章内容',
  `article_pub_time` DATETIME DEFAULT '1000-01-01 00:00:00' COMMENT '文章发布时间',
  `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY idx_task_id (`task_id`),
  UNIQUE KEY idx_platform_article_id (`platform_id`, `article_id`),
  KEY idx_platform_author_id (`platform_id`, `article_author_id`),
  KEY idx_article_pub_time (`article_pub_time`),
  KEY idx_create_time (`create_time`),
  KEY idx_update_time (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='抓取结果表';


CREATE TABLE `log_task_scheduling` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `platform_id` TINYINT DEFAULT 0 COMMENT '平台id（1:微信;2:微博;3:头条）',
  `platform_name` VARCHAR(50) DEFAULT '' COMMENT '平台名称（1:微信;2:微博;3:头条）',
  `spider_name` VARCHAR(45) DEFAULT '' COMMENT '蜘蛛名称，一般同平台名称',
  `task_quantity` INT(11) DEFAULT 0 COMMENT '任务数量',
  `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务调度日志表';

-- 更新记录[2018-02-13]
# ALTER TABLE `fetch_result` MODIFY `article_content` MEDIUMTEXT COMMENT '文章内容';

-- 更新记录[2018-05-29]
# DROP INDEX idx_platform_author_id ON `fetch_result`;
# ALTER TABLE `fetch_result` ADD INDEX idx_platform_author_id (`platform_id`, `article_author_id`);
# ALTER TABLE `fetch_result` MODIFY `article_pub_time` DATETIME DEFAULT '1000-01-01 00:00:00' COMMENT '文章发布时间';
# ALTER TABLE `fetch_result` ADD INDEX idx_article_pub_time (`article_pub_time`);
# ALTER TABLE `fetch_result` ADD INDEX idx_create_time (`create_time`);
# ALTER TABLE `fetch_result` ADD INDEX idx_update_time (`update_time`);
