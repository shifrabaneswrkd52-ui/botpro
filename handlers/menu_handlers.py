from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from services.schedule_service import schedule_service

from config import NEWSPAPERS
from database.json_manager import load_channels, load_sources, save_sources
from database.rss_manager import get_rss_feed_info
from datetime import datetime

def main_menu(update: Update, context: CallbackContext):
    """Hiển thị menu chính hoàn chỉnh"""
    keyboard = [
        [InlineKeyboardButton("📺 Quản lý kênh", callback_data="manage_channels"),
         InlineKeyboardButton("📰 Quản lý nguồn tin", callback_data="manage_articles")],
        [InlineKeyboardButton("⏰ Quản lý lịch đăng", callback_data="manage_schedules"),
         InlineKeyboardButton("📢 Quản lý quảng cáo", callback_data="manage_ads")],
        [InlineKeyboardButton("👁️ Xem bài viết", callback_data="view_articles"),
         InlineKeyboardButton("📋 Bài đã đăng", callback_data="view_posted_articles")],
        [InlineKeyboardButton("📊 Thống kê", callback_data="view_stats"),
         InlineKeyboardButton("💾 Backup", callback_data="manage_backup")],
        [InlineKeyboardButton("🔄 Cập nhật", callback_data="check_updates")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        update.callback_query.edit_message_text("🤖 Menu chính - Telegram RSS Bot", reply_markup=reply_markup)
    else:
        update.message.reply_text("🤖 Menu chính - Telegram RSS Bot", reply_markup=reply_markup)

def manage_channels(update: Update, context: CallbackContext):
    """Quản lý kênh"""
    if update.callback_query:
        query = update.callback_query
        query.answer()
        edit_message = query.edit_message_text
    else:
        edit_message = update.message.reply_text

    channels = load_channels()
    keyboard = []
    if channels:
        for chat_id, info in channels.items():
            keyboard.append([InlineKeyboardButton(f"{info['title']} ({chat_id})", callback_data=f"channel_{chat_id}")])
    keyboard.append([InlineKeyboardButton("➕ Thêm kênh", callback_data="add_channel")])
    keyboard.append([InlineKeyboardButton("🔙 Trở lại", callback_data="back_main")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    edit_message("📌 Quản lý kênh:", reply_markup=reply_markup)

def manage_articles(update: Update, context: CallbackContext):
    """Quản lý nguồn tin RSS"""
    query = update.callback_query
    query.answer()
    
    # Tạo keyboard 2 hàng, mỗi hàng 4 nút (tổng 8 nút) cho các báo
    keyboard = []
    row = []
    
    newspapers = list(NEWSPAPERS.keys())
    for i, newspaper in enumerate(newspapers, 1):
        row.append(InlineKeyboardButton(f"{i}", callback_data=f"newspaper_{newspaper}"))
        if i % 4 == 0:
            keyboard.append(row)
            row = []
    
    # Thêm nút quay lại
    keyboard.append([InlineKeyboardButton("🔙 Trở lại", callback_data="back_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        "📰 Chọn báo để quản lý nguồn tin:\n\n" +
        "\n".join([f"{i}. {paper}" for i, paper in enumerate(newspapers, 1)]),
        reply_markup=reply_markup
    )

def newspaper_categories(update: Update, context: CallbackContext, newspaper_name: str):
    """Hiển thị chuyên mục của báo"""
    query = update.callback_query
    query.answer()
    
    if newspaper_name not in NEWSPAPERS:
        query.edit_message_text("⚠️ Báo không tồn tại.")
        return
    
    categories = NEWSPAPERS[newspaper_name]
    
    # Tạo keyboard cho các chuyên mục
    keyboard = []
    row = []
    
    for i, (category_name, rss_url) in enumerate(categories.items(), 1):
        row.append(InlineKeyboardButton(category_name, callback_data=f"category_{newspaper_name}_{category_name}"))
        if i % 2 == 0:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("↩️ Trở lại", callback_data="manage_articles")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        f"📋 Chuyên mục của {newspaper_name}:\n\n"
        "Chọn chuyên mục để thêm làm nguồn tin:",
        reply_markup=reply_markup
    )

def handle_category_selection(update: Update, context: CallbackContext, newspaper_name: str, category_name: str):
    """Xử lý khi chọn chuyên mục"""
    query = update.callback_query
    query.answer()
    
    if newspaper_name not in NEWSPAPERS or category_name not in NEWSPAPERS[newspaper_name]:
        query.edit_message_text("⚠️ Chuyên mục không tồn tại.")
        return
    
    rss_url = NEWSPAPERS[newspaper_name][category_name]
    
    # Kiểm tra RSS feed
    feed_info = get_rss_feed_info(rss_url)
    
    if not feed_info.get('is_valid'):
        query.edit_message_text(
            f"❌ RSS feed không hợp lệ:\n\n"
            f"📰 Báo: {newspaper_name}\n"
            f"📋 Chuyên mục: {category_name}\n"
            f"🔗 URL: {rss_url}\n\n"
            f"Lỗi: {feed_info.get('error', 'Không xác định')}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("↩️ Trở lại", callback_data=f"newspaper_{newspaper_name}")]
            ])
        )
        return
    
    # Lưu RSS feed vào sources.json
    sources = load_sources()
    source_id = f"{newspaper_name}_{category_name}"
    
    if source_id not in sources:
        sources[source_id] = {
            'newspaper': newspaper_name,
            'category': category_name,
            'rss_url': rss_url,
            'title': feed_info['title'],
            'description': feed_info['description'],
            'link': feed_info['link'],
            'added_date': str(datetime.now())
        }
        save_sources(sources)
        
        query.edit_message_text(
            f"✅ Đã thêm nguồn tin:\n\n"
            f"📰 Báo: {newspaper_name}\n"
            f"📋 Chuyên mục: {category_name}\n"
            f"📝 Tiêu đề: {feed_info['title']}\n"
            f"📊 Số bài: {feed_info['entries_count']}\n"
            f"🔗 URL: {rss_url}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📰 Thêm chuyên mục khác", callback_data=f"newspaper_{newspaper_name}")],
                [InlineKeyboardButton("🔙 Quản lý nguồn tin", callback_data="manage_articles")]
            ])
        )
    else:
        query.edit_message_text(
            f"⚠️ Nguồn tin đã tồn tại:\n\n"
            f"📰 Báo: {newspaper_name}\n"
            f"📋 Chuyên mục: {category_name}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📰 Thêm chuyên mục khác", callback_data=f"newspaper_{newspaper_name}")],
                [InlineKeyboardButton("🔙 Quản lý nguồn tin", callback_data="manage_articles")]
            ])
        )

def view_sources(update: Update, context: CallbackContext):
    """Xem danh sách nguồn tin đã thêm"""
    query = update.callback_query
    query.answer()
    
    sources = load_sources()
    
    if not sources:
        query.edit_message_text(
            "📋 Chưa có nguồn tin nào được thêm.\n\n"
            "Hãy thêm nguồn tin từ menu quản lý nguồn tin.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📰 Quản lý nguồn tin", callback_data="manage_articles")],
                [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
            ])
        )
        return
    
    message = "📋 Danh sách nguồn tin đã thêm:\n\n"
    for source_id, source_info in sources.items():
        feed_info = get_rss_feed_info(source_info['rss_url'])
        message += f"📰 {source_info['newspaper']} - {source_info['category']}\n"
        message += f"🔗 {source_info['rss_url']}\n"
        message += f"📊 Bài viết: {feed_info.get('entries_count', 0)}\n"
        message += "─" * 30 + "\n"
    
    query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🗑️ Xóa nguồn tin", callback_data="delete_sources")],
            [InlineKeyboardButton("📰 Quản lý nguồn tin", callback_data="manage_articles")],
            [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
        ])
    )

def delete_channel(update: Update, context: CallbackContext, channel_id: str):
    """Xóa kênh khỏi danh sách"""
    query = update.callback_query
    query.answer()
    
    from database.json_manager import load_channels, save_channels
    channels = load_channels()
    if channel_id in channels:
        del channels[channel_id]
        save_channels(channels)
        query.edit_message_text(f"✅ Đã xóa kênh {channel_id}")
    else:
        query.edit_message_text("⚠️ Kênh không tồn tại.")
    
    manage_channels(update, context)

def delete_source(update: Update, context: CallbackContext, source_id: str):
    """Xóa nguồn tin"""
    query = update.callback_query
    query.answer()
    
    from database.json_manager import load_sources, save_sources
    sources = load_sources()
    if source_id in sources:
        del sources[source_id]
        save_sources(sources)
        query.edit_message_text(f"✅ Đã xóa nguồn tin: {source_id}")
    else:
        query.edit_message_text("⚠️ Nguồn tin không tồn tại.")
    
    view_sources(update, context)
def view_articles(update: Update, context: CallbackContext):
    """Xem bài viết mới nhất từ các nguồn"""
    query = update.callback_query
    query.answer()
    
    from services.article_service import get_articles_from_sources
    articles = get_articles_from_sources(5)
    
    if not articles:
        query.edit_message_text(
            "📰 Chưa có bài viết nào.\n\n"
            "Hãy thêm nguồn tin và chờ bài viết mới.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📰 Quản lý nguồn tin", callback_data="manage_articles")],
                [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
            ])
        )
        return
    
    message = "📰 Bài viết mới nhất:\n\n"
    for i, article in enumerate(articles, 1):
        message += f"{i}. {article['title']}\n"
        message += f"   📰 Nguồn: {article['source']} - {article['category']}\n"
        message += f"   📅 {article.get('published', 'Không có ngày')}\n"
        message += "─" * 40 + "\n"
    
    query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Làm mới", callback_data="view_articles")],
            [InlineKeyboardButton("📰 Quản lý nguồn tin", callback_data="manage_articles")],
            [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
        ])
    )

def manage_schedules(update: Update, context: CallbackContext, channel_id=None):
    """Quản lý lịch đăng bài"""
    query = update.callback_query
    query.answer()
    
    channels = load_channels()
    
    if not channels:
        query.edit_message_text(
            "⚠️ Chưa có kênh nào được thêm.\n\n"
            "Hãy thêm kênh trước khi thiết lập lịch đăng bài.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📌 Thêm kênh", callback_data="add_channel")],
                [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
            ])
        )
        return
    
    keyboard = []
    for chat_id, channel_info in channels.items():
        keyboard.append([InlineKeyboardButton(
            f"📺 {channel_info['title']}", 
            callback_data=f"channel_schedule_{chat_id}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        "⏰ Quản lý lịch đăng bài:\n\n"
        "Chọn kênh để thiết lập lịch đăng bài tự động:",
        reply_markup=reply_markup
    )

def channel_schedule_menu(update: Update, context: CallbackContext, channel_id: str):
    """Menu lịch đăng bài cho kênh cụ thể"""
    query = update.callback_query
    query.answer()
    
    channels = load_channels()
    channel_info = channels.get(channel_id, {})
    
    from services.schedule_service import schedule_service
    channel_schedules = schedule_service.get_channel_schedules(channel_id)
    
    message = f"⏰ Lịch đăng bài cho: {channel_info.get('title', channel_id)}\n\n"
    
    if channel_schedules:
        for schedule_id, schedule in channel_schedules.items():
            interval = schedule['interval_seconds']
            interval_text = f"{interval//3600} giờ" if interval >= 3600 else f"{interval//60} phút"
            status = "✅ Bật" if schedule['enabled'] else "❌ Tắt"
            message += f"• {interval_text} - {status}\n"
    else:
        message += "📭 Chưa có lịch đăng bài nào\n"
    
    keyboard = [
        [InlineKeyboardButton("🔄 5 phút", callback_data=f"add_schedule_{channel_id}_300")],
        [InlineKeyboardButton("🔄 15 phút", callback_data=f"add_schedule_{channel_id}_900")],
        [InlineKeyboardButton("🔄 30 phút", callback_data=f"add_schedule_{channel_id}_1800")],
        [InlineKeyboardButton("🔄 1 giờ", callback_data=f"add_schedule_{channel_id}_3600")],
        [InlineKeyboardButton("🗑️ Xóa lịch", callback_data=f"delete_schedules_{channel_id}")],
        [InlineKeyboardButton("🔙 Quay lại", callback_data="manage_schedules")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)

def show_dashboard(update: Update, context: CallbackContext):
    """Hiển thị dashboard tổng quan"""
    query = update.callback_query
    query.answer()
    
    channels = load_channels()
    sources = load_sources()
    from services.schedule_service import schedule_service
    schedules = schedule_service.get_all_schedules()
    from services.stats_service import stats_service
    stats = stats_service.get_daily_stats()
    
    active_schedules = sum(1 for s in schedules.values() if s['enabled'])
    
    message = "📊 Dashboard Tổng quan\n\n"
    message += f"📺 Số kênh: {len(channels)}\n"
    message += f"📰 Số nguồn tin: {len(sources)}\n"
    message += f"⏰ Lịch đăng bài: {active_schedules} hoạt động\n"
    message += f"📈 Bài đã đăng: {stats['total_posts']}\n"
    message += f"📢 Quảng cáo đã đăng: {stats['total_ads']}\n"
    message += f"📅 Hôm nay: {stats['daily_posts']} bài + {stats['daily_ads']} quảng cáo\n\n"
    message += "💡 Chọn chức năng từ menu bên dưới:"
    
    keyboard = [
        [InlineKeyboardButton("📺 Quản lý kênh", callback_data="manage_channels")],
        [InlineKeyboardButton("📰 Quản lý nguồn tin", callback_data="manage_articles")],
        [InlineKeyboardButton("⏰ Quản lý lịch đăng", callback_data="manage_schedules")],
        [InlineKeyboardButton("📢 Quản lý quảng cáo", callback_data="manage_ads")],
        [InlineKeyboardButton("👁️ Xem bài viết", callback_data="view_articles")],
        [InlineKeyboardButton("📊 Xem thống kê", callback_data="view_stats")],
        [InlineKeyboardButton("🔄 Làm mới", callback_data="dashboard")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)

def manage_ads(update: Update, context: CallbackContext):
    """Quản lý quảng cáo"""
    query = update.callback_query
    query.answer()
    
    from services.ad_service import ad_service
    ads = ad_service.get_all_ads()
    
    message = "📢 Quản lý Quảng cáo\n\n"
    
    if ads:
        for ad_id, ad_info in ads.items():
            status = "✅" if ad_info['is_active'] else "❌"
            message += f"{status} {ad_info['title']} (Đã đăng: {ad_info['times_posted']})\n"
    else:
        message += "📭 Chưa có quảng cáo nào\n"
    
    keyboard = [
        [InlineKeyboardButton("➕ Tạo quảng cáo", callback_data="create_ad")],
        [InlineKeyboardButton("📋 Danh sách quảng cáo", callback_data="list_ads")],
        [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)

def create_ad_menu(update: Update, context: CallbackContext):
    """Menu tạo quảng cáo mới"""
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        "📝 Tạo quảng cáo mới:\n\n"
        "Vui lòng gửi nội dung quảng cáo theo định dạng:\n"
        "Tiêu đề|Nội dung\n\n"
        "Ví dụ:\n"
        "Khuyến mãi đặc biệt|Giảm giá 50% cho tất cả sản phẩm. Liên hệ ngay!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Quay lại", callback_data="manage_ads")]
        ])
    )
    
def view_stats(update: Update, context: CallbackContext):
    """Xem thống kê chi tiết"""
    query = update.callback_query
    query.answer()
    
    from services.stats_service import stats_service
    from database.json_manager import load_channels
    
    daily_stats = stats_service.get_daily_stats()
    source_stats = stats_service.get_source_stats()
    channel_stats = stats_service.get_channel_stats()
    
    message = "📊 Thống kê chi tiết\n\n"
    message += f"📈 Hôm nay: {daily_stats['daily_posts']} bài + {daily_stats['daily_ads']} quảng cáo\n"
    message += f"📊 Tổng: {daily_stats['total_posts']} bài + {daily_stats['total_ads']} quảng cáo\n\n"
    
    message += "📰 Top nguồn tin:\n"
    for source, count in list(source_stats.items())[:5]:
        message += f"• {source}: {count} bài\n"
    
    message += "\n📺 Top kênh:\n"
    channels = load_channels()
    for channel_id, count in list(channel_stats.items())[:3]:
        channel_name = channels.get(channel_id, {}).get('title', channel_id)
        message += f"• {channel_name}: {count} bài\n"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Làm mới", callback_data="view_stats")],
        [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)

def list_ads(update: Update, context: CallbackContext):
    """Hiển thị danh sách quảng cáo"""
    query = update.callback_query
    query.answer()
    
    from services.ad_service import ad_service
    ads = ad_service.get_all_ads()
    
    message = "📢 Danh sách Quảng cáo\n\n"
    
    if ads:
        for ad_id, ad in ads.items():
            status = "✅" if ad['is_active'] else "❌"
            message += f"{status} {ad['title']} (Đã đăng: {ad['times_posted']})\n"
    else:
        message += "📭 Chưa có quảng cáo nào\n"
    
    keyboard = [
        [InlineKeyboardButton("➕ Tạo quảng cáo", callback_data="create_ad")],
        [InlineKeyboardButton("🔙 Quay lại", callback_data="manage_ads")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup) 

def view_posted_articles(update: Update, context: CallbackContext):
    """Xem bài viết đã đăng"""
    query = update.callback_query
    query.answer()
    
    from database.json_manager import load_posted
    posted = load_posted()
    
    if not posted:
        query.edit_message_text(
            "📭 Chưa có bài viết nào được đăng.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
            ])
        )
        return
    
    message = "📋 Bài viết đã đăng:\n\n"
    for i, (article_id, article_info) in enumerate(list(posted.items())[-10:], 1):
        message += f"{i}. {article_info['title']}\n"
        message += f"   📰 {article_info['source']} - {article_info['category']}\n"
        message += f"   📅 {article_info['posted_at'][:16]}\n"
        message += "─" * 40 + "\n"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Làm mới", callback_data="view_posted_articles")],
        [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)

def channel_detail_menu(update: Update, context: CallbackContext, channel_id: str):
    """Menu chi tiết cho kênh"""
    query = update.callback_query
    query.answer()
    
    channels = load_channels()
    channel_info = channels.get(channel_id, {})
    
    keyboard = [
        [InlineKeyboardButton("📊 Xem thống kê", callback_data=f"stats_{channel_id}")],
        [InlineKeyboardButton("⚙️ Cài đặt", callback_data=f"settings_{channel_id}")],
        [InlineKeyboardButton("🗑️ Xóa kênh", callback_data=f"delete_channel_{channel_id}")],
        [InlineKeyboardButton("🔙 Quay lại", callback_data="manage_channels")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        f"📺 Chi tiết kênh: {channel_info.get('title', channel_id)}\n\n"
        f"👤 Username: {channel_info.get('username', 'N/A')}\n"
        f"📅 Ngày thêm: {channel_info.get('added_date', 'N/A')}",
        reply_markup=reply_markup
    )


def manage_backup(update: Update, context: CallbackContext):
    """Quản lý backup"""
    query = update.callback_query
    query.answer()
    
    from services.backup_service import backup_service
    backups = backup_service.list_backups()
    
    message = "💾 Quản lý Backup\n\n"
    
    if backups:
        message += "📦 Danh sách backup:\n"
        for i, backup in enumerate(backups[:5], 1):
            message += f"{i}. {backup['created_at']}\n"
    else:
        message += "📭 Chưa có backup nào\n"
    
    keyboard = [
        [InlineKeyboardButton("➕ Tạo backup", callback_data="create_backup")],
        [InlineKeyboardButton("🔄 Khôi phục", callback_data="restore_backup_menu")],
        [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)

def restore_backup_menu(update: Update, context: CallbackContext):
    """Menu khôi phục backup"""
    query = update.callback_query
    query.answer()
    
    from services.backup_service import backup_service
    backups = backup_service.list_backups()
    
    if not backups:
        query.edit_message_text("📭 Chưa có backup nào để khôi phục")
        return
    
    keyboard = []
    for backup in backups[:5]:  # Hiển thị tối đa 5 backup
        keyboard.append([InlineKeyboardButton(
            backup['created_at'], 
            callback_data=f"restore_{backup['name']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Quay lại", callback_data="manage_backup")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("📦 Chọn backup để khôi phục:", reply_markup=reply_markup)

def manage_backup(update: Update, context: CallbackContext):
    """Quản lý backup"""
    query = update.callback_query
    query.answer()
    
    from services.backup_service import backup_service
    backups = backup_service.list_backups()
    
    message = "💾 Quản lý Backup\n\n"
    
    if backups:
        message += "📦 Danh sách backup:\n"
        for i, backup in enumerate(backups[:5], 1):
            message += f"{i}. {backup['created_at']}\n"
    else:
        message += "📭 Chưa có backup nào\n"
    
    keyboard = [
        [InlineKeyboardButton("➕ Tạo backup", callback_data="create_backup")],
        [InlineKeyboardButton("🔄 Khôi phục", callback_data="restore_backup_menu")],
        [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)

def restore_backup_menu(update: Update, context: CallbackContext):
    """Menu khôi phục backup"""
    query = update.callback_query
    query.answer()
    
    from services.backup_service import backup_service
    backups = backup_service.list_backups()
    
    if not backups:
        query.edit_message_text("📭 Chưa có backup nào để khôi phục")
        return
    
    keyboard = []
    for backup in backups[:5]:  # Hiển thị tối đa 5 backup
        keyboard.append([InlineKeyboardButton(
            backup['created_at'], 
            callback_data=f"restore_{backup['name']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Quay lại", callback_data="manage_backup")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("📦 Chọn backup để khôi phục:", reply_markup=reply_markup)

    # Lưu trạng thái để xử lý trong message handler
    user_id = str(query.from_user.id)
    user_state[user_id] = "creating_ad"
