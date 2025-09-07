# ---------------------------------------------------
# File Name: start.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import filters
from devgagan import app
from config import OWNER_ID 
from devgagan.core.func import subscribe
import asyncio
from devgagan.core.func import *
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.raw.functions.bots import SetBotInfo
from pyrogram.raw.types import InputUserSelf

from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from devgagan.core.mongo.plans_db import get_all_users
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
from datetime import datetime

@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("token", "🎲 Get 3 hours free access"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("freez", "🧊 Remove all expired user"),
        BotCommand("pay", "₹ Pay now to get subscription"),
        BotCommand("status", "⟳ Refresh Payment status"),
        BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("myplan", "⌛ Get your plan details"),
        BotCommand("add", "➕ Add user to premium"),
        BotCommand("rem", "➖ Remove from premium"),
        BotCommand("session", "🧵 Generate Pyrogramv2 session"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("stats", "📊 Get stats of the bot"),
        BotCommand("plan", "🗓️ Check our premium plans"),
        BotCommand("terms", "🥺 Terms and conditions"),
        BotCommand("speedtest", "🚅 Speed of server"),
        BotCommand("lock", "🔒 Protect channel from extraction"),
        BotCommand("gcast", "⚡ Broadcast message to bot users"),
        BotCommand("help", "❓ If you're a noob, still!"),
        BotCommand("cancel", "🚫 Cancel batch process")
    ])

    await message.reply("✅ Commands configured successfully!")




help_pages = [
    (
        "📝 **Bot Commands Overview (1/2)**:\n\n"
        "1. **/add userID**\n"
        "> Add user to premium (Owner only)\n\n"
        "2. **/rem userID**\n"
        "> Remove user from premium (Owner only)\n\n"
        "3. **/transfer userID**\n"
        "> Transfer premium to your beloved major purpose for resellers (Premium members only)\n\n"
        "4. **/get**\n"
        "> Get all user IDs (Owner only)\n\n"
        "5. **/lock**\n"
        "> Lock channel from extraction (Owner only)\n\n"
        "6. **/dl link**\n"
        "> Download videos (Not available in v3 if you are using)\n\n"
        "7. **/adl link**\n"
        "> Download audio (Not available in v3 if you are using)\n\n"
        "8. **/login**\n"
        "> Log into the bot for private channel access\n\n"
        "9. **/batch**\n"
        "> Bulk extraction for posts (After login)\n\n"
    ),
    (
        "📝 **Bot Commands Overview (2/2)**:\n\n"
        "10. **/logout**\n"
        "> Logout from the bot\n\n"
        "11. **/stats**\n"
        "> Get bot stats\n\n"
        "12. **/plan**\n"
        "> Check premium plans\n\n"
        "13. **/speedtest**\n"
        "> Test the server speed (not available in v3)\n\n"
        "14. **/terms**\n"
        "> Terms and conditions\n\n"
        "15. **/cancel**\n"
        "> Cancel ongoing batch process\n\n"
        "16. **/myplan**\n"
        "> Get details about your plans\n\n"
        "17. **/session**\n"
        "> Generate Pyrogram V2 session\n\n"
        "18. **/settings**\n"
        "> 1. SETCHATID : To directly upload in channel or group or user's dm use it with -100[chatID]\n"
        "> 2. SETRENAME : To add custom rename tag or username of your channels\n"
        "> 3. CAPTION : To add custom caption\n"
        "> 4. REPLACEWORDS : Can be used for words in deleted set via REMOVE WORDS\n"
        "> 5. RESET : To set the things back to default\n\n"
        "> You can set CUSTOM THUMBNAIL, PDF WATERMARK, VIDEO WATERMARK, SESSION-based login, etc. from settings\n\n"
        "**__Powered by Team SPY__**"
    )
]


async def send_or_edit_help_page(_, message, page_number, is_callback=False):
    if page_number < 0 or page_number >= len(help_pages):
        return


    prev_button = InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}")


    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)


    keyboard = InlineKeyboardMarkup([buttons])

    # If this is from a callback query, edit the message
    if is_callback:
        await message.edit_text(
            help_pages[page_number],
            reply_markup=keyboard
        )
    else:
        # If this is the initial help command, send a new message
        await message.reply(
            help_pages[page_number],
            reply_markup=keyboard
        )


@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return


    await send_or_edit_help_page(client, message, 0)


@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])

    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1


    await send_or_edit_help_page(client, callback_query.message, page_number, is_callback=True)


    await callback_query.answer()


@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/kingofpatal")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)


@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = (
        "> 💰 **Premium Price**:\n\n Starting from $2 or 200 INR accepted via **__Amazon Gift Card__** (terms and conditions apply).\n"
        "📥 **Download Limit**: Users can download up to 100,000 files in a single batch command.\n"
        "🛑 **Batch**: You will get two modes /bulk and /batch.\n"
        "   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms.\n"
    )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/kingofpatal")],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "> 💰**Premium Price**\n\n Starting from $2 or 200 INR accepted via **__Amazon Gift Card__** (terms and conditions apply).\n"
        "📥 **Download Limit**: Users can download up to 100,000 files in a single batch command.\n"
        "🛑 **Batch**: You will get two modes /bulk and /batch.\n"
        "   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms or click See Terms👇\n"
    )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/")],
        ]
    )
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/kingofpatal")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)


@app.on_message(filters.command("get"))
async def get_all_user_ids(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("❌ You are not authorized to use this command.")
        return

    try:
        # Send initial message
        status_msg = await message.reply("📋 Generating comprehensive user details PDF...")

        # Import the new function
        from devgagan.core.mongo.plans_db import get_user_info_with_names
        
        users = await get_user_info_with_names(app)
        if not users:
            await status_msg.edit("📭 No users found in the database.")
            return

        # Create PDF file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"user_details_report_{timestamp}.pdf"
        pdf_path = f"/tmp/{pdf_filename}"

        # Create PDF document with better margins
        doc = SimpleDocTemplate(pdf_path, pagesize=A4, 
                              leftMargin=0.75*inch, rightMargin=0.75*inch,
                              topMargin=1*inch, bottomMargin=1*inch)
        styles = getSampleStyleSheet()
        story = []

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        page_title_style = ParagraphStyle(
            'PageTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=1,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        )
        
        section_style = ParagraphStyle(
            'Section',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            textColor=colors.darkred,
            fontName='Helvetica-Bold'
        )

        # Cover Page
        story.append(Paragraph("📊 Telegram Bot Analytics Report", title_style))
        story.append(Spacer(1, 20))
        
        cover_info = [
            ["📅 Report Date:", datetime.now().strftime("%B %d, %Y")],
            ["⏰ Generated At:", datetime.now().strftime("%H:%M:%S UTC")],
            ["📊 Total Users:", str(len(users))],
            ["🤖 Bot Version:", "v2.0.5"],
            ["👨‍💻 Generated By:", "Admin Dashboard"]
        ]
        
        cover_table = Table(cover_info, colWidths=[2.5*inch, 3*inch])
        cover_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.darkblue),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.lightblue, colors.white])
        ]))
        
        story.append(cover_table)
        story.append(Spacer(1, 40))
        
        # Table of Contents
        story.append(Paragraph("📋 Table of Contents", section_style))
        toc_data = [
            ["1.", "Summary Statistics", "Page 2"],
            ["2.", "All Users Overview", "Page 3"],
            ["3.", "Premium Users Details", "Page 4"],
            ["4.", "Free Users List", "Page 5"],
            ["5.", "Daily Usage Analytics", "Page 6"]
        ]
        
        toc_table = Table(toc_data, colWidths=[0.5*inch, 3*inch, 1.5*inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(toc_table)
        
        from reportlab.platypus import PageBreak
        story.append(PageBreak())

        # Prepare data
        premium_users = []
        free_users = []
        premium_count = 0
        free_count = 0
        current_time = datetime.utcnow()

        for user in users:
            user_id = user.get('_id')
            expire_date = user.get('expire_date')
            user_name = user.get('user_name', f"User_{str(user_id)[-4:]}")
            
            if expire_date and expire_date > current_time:
                premium_count += 1
                expire_str = expire_date.strftime("%Y-%m-%d %H:%M")
                days_left = (expire_date - current_time).days
                premium_users.append([str(user_id), user_name, expire_str, f"{days_left} days"])
            else:
                free_count += 1
                free_users.append([str(user_id), user_name, "No Premium", "Free User"])

        # Page 1: Summary Statistics
        story.append(Paragraph("📈 Summary Statistics", page_title_style))
        story.append(Spacer(1, 20))

        summary_data = [
            ["📊 Metric", "📈 Value", "📋 Description"],
            ["👥 Total Users", str(len(users)), "All registered users"],
            ["💎 Premium Users", str(premium_count), f"{(premium_count/len(users)*100):.1f}% of total users"],
            ["🆓 Free Users", str(free_count), f"{(free_count/len(users)*100):.1f}% of total users"],
            ["📅 Active Today", "N/A", "Users active in last 24h"],
            ["💰 Revenue Users", str(premium_count), "Users contributing to revenue"],
            ["📊 Conversion Rate", f"{(premium_count/len(users)*100):.1f}%", "Free to Premium conversion"]
        ]

        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightblue, colors.white]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(summary_table)
        story.append(PageBreak())

        # Page 2: All Users Overview
        story.append(Paragraph("👥 All Users Overview", page_title_style))
        story.append(Spacer(1, 20))

        all_users_data = [["User ID", "Username", "Status", "Expiry/Type"]]
        for user in users:
            user_id = user.get('_id')
            expire_date = user.get('expire_date')
            user_name = user.get('user_name', f"User_{str(user_id)[-4:]}")
            
            if expire_date and expire_date > current_time:
                status = "💎 Premium"
                expire_str = expire_date.strftime("%Y-%m-%d")
            else:
                status = "🆓 Free"
                expire_str = "Free User"
                
            all_users_data.append([str(user_id), user_name, status, expire_str])

        all_users_table = Table(all_users_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        all_users_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgreen, colors.white]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(all_users_table)
        story.append(PageBreak())

        # Page 3: Premium Users Details
        story.append(Paragraph("💎 Premium Users Details", page_title_style))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph(f"Total Premium Users: {premium_count}", section_style))
        story.append(Spacer(1, 10))

        if premium_users:
            premium_data = [["User ID", "Username", "Expiry Date", "Days Left"]]
            premium_data.extend(premium_users)

            premium_table = Table(premium_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            premium_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gold),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightyellow, colors.white]),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            story.append(premium_table)
        else:
            story.append(Paragraph("No premium users found.", styles['Normal']))
        
        story.append(PageBreak())

        # Page 4: Free Users List
        story.append(Paragraph("🆓 Free Users List", page_title_style))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph(f"Total Free Users: {free_count}", section_style))
        story.append(Spacer(1, 10))

        if free_users:
            # Split free users into chunks for better page layout
            chunk_size = 25
            for i in range(0, len(free_users), chunk_size):
                chunk = free_users[i:i + chunk_size]
                free_data = [["User ID", "Username", "Status", "Type"]]
                free_data.extend(chunk)

                free_table = Table(free_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
                free_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightcoral),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.mistyrose, colors.white]),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                ]))
                story.append(free_table)
                story.append(Spacer(1, 20))
        else:
            story.append(Paragraph("No free users found.", styles['Normal']))
        
        story.append(PageBreak())

        # Page 5: Daily Usage Analytics
        story.append(Paragraph("📊 Daily Usage Analytics", page_title_style))
        story.append(Spacer(1, 20))

        # Simulated daily usage data
        usage_data = [
            ["📅 Date", "👥 Active Users", "📥 Downloads", "💎 New Premium", "🔄 Conversions"],
            [datetime.now().strftime("%Y-%m-%d"), "N/A", "N/A", "N/A", "N/A"],
            ["Previous Days", "Coming Soon", "Coming Soon", "Coming Soon", "Coming Soon"]
        ]

        usage_table = Table(usage_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        usage_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lavender, colors.white]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(usage_table)
        
        story.append(Spacer(1, 30))
        story.append(Paragraph("📝 Note: Daily usage analytics will be implemented in future updates.", styles['Italic']))

        # Build PDF
        doc.build(story)

        # Send PDF file
        await status_msg.edit("📤 Uploading comprehensive PDF report...")

        with open(pdf_path, 'rb') as pdf_file:
            await message.reply_document(
                document=pdf_file,
                caption=f"📊 **Comprehensive User Analytics Report**\n\n"
                       f"📈 **Summary:**\n"
                       f"👥 Total Users: {len(users)}\n"
                       f"💎 Premium Users: {premium_count}\n"
                       f"🆓 Free Users: {free_count}\n"
                       f"📊 Conversion Rate: {(premium_count/len(users)*100):.1f}%\n\n"
                       f"📋 **Report Contains:**\n"
                       f"• Summary Statistics\n"
                       f"• All Users Overview\n"
                       f"• Premium Users Details\n"
                       f"• Free Users List\n"
                       f"• Daily Usage Analytics\n\n"
                       f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                file_name=pdf_filename
            )

        # Clean up
        os.remove(pdf_path)
        await status_msg.delete()

    except Exception as e:
        await message.reply(f"❌ Error generating PDF: {str(e)}")n("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/kingofpatal")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)
 
 
