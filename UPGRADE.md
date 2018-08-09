# 1. update subscription_subscribedemail database #

alter table subscription_subscribedemail add is_spam int default 0;

alter table subscription_subscribedemail add index (is_spam);


# 2. developer settings #

add NEWTON_DEV_URL