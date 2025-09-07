 
# ---------------------------------------------------
# File Name: shrink.py
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

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
import string
import aiohttp
from devgagan import app
from devgagan.core.func import *
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, START_IMAGE_URL, WEBSITE_URL, AD_API, LOG_GROUP  
 
 
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]
 
 
async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)
 
 
 
Param = {}
 
 
async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
 
 
async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
 
     
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()   
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None
 
 
async def is_user_verified(user_id):
    """Check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None
 
 
@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """Handle the /token command."""
    join = await subscribe(client, message)
    if join == 1:
        return
    user_id = message.chat.id
    if len(message.command) <= 1:
        join_button = InlineKeyboardButton("𝐉𝐨𝐢𝐧 𝐌𝐚𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url="https://t.me/wabxbots/3")
        premium = InlineKeyboardButton("𝐑𝐞𝐩𝐨𝐫𝐭 𝐄𝐫𝐫𝐨𝐫𝐬", url="https://t.me/")
        help_button = InlineKeyboardButton("Help", callback_data="help_callback")
        features_button = InlineKeyboardButton("Features", callback_data="features_callback")
        keyboard = InlineKeyboardMarkup([
            [join_button],   
            [premium],
            [help_button, features_button]    
        ])
         
        await message.reply_photo(
            START_IMAGE_URL,
            caption=(
                f"Hi {message.from_user.mention} 👋 Welcome, Wanna intro...?\n\n"
                "**➭ Sᴀᴠᴇ ᴘᴏꜱᴛꜱ ғʀᴏᴍ ᴄʜᴀɴɴᴇʟꜱ ᴀɴᴅ ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ғᴏʀᴡᴀʀᴅɪɴɢ ɪꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ**\n"
                "**➭ Eᴀꜱɪʟʏ ғᴇᴛᴄʜ ᴍᴇꜱꜱᴀɢᴇꜱ ғʀᴏᴍ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ ʙʏ ꜱᴇɴᴅɪɴɢ ᴛʜᴇɪʀ ᴘᴏꜱᴛ ʟɪɴᴋꜱ**\n"
                "**➭ Fᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ, ᴜꜱᴇ /ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇꜱꜱ ᴄᴏɴᴛᴇɴᴛ ꜱᴇᴄᴜʀᴇʟʏ**\n\n"
                "**📑 Fᴏʀ ᴍᴏʀᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ ꜱᴇɴᴅ /help**"
            ),
            reply_markup=keyboard
        )
        return  
 
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
 
     
    if param:
        if user_id in Param and Param[user_id] == param:
             
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            })
            del Param[user_id]   
            await message.reply("✅ You have been verified successfully! Enjoy your session for next 3 hours.")
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return
 
@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
     
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
    if await is_user_verified(user_id):
        await message.reply("✅ Your free session is already active enjoy!")
    else:
         
        param = await generate_random_param()
        Param[user_id] = param   
 
         
        deep_link = f"https://t.me/{client.me.username}?start={param}"
 
         
        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return
 
         
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Verify the token now...", url=shortened_url)]]
        )
        await message.reply("Click the button below to verify your free access token: \n\n> What will you get ? \n1. No time bound upto 3 hours \n2. Batch command limit will be FreeLimit + 20 \n3. All functions unlocked", reply_markup=button)
 
@app.on_callback_query(filters.regex("help_callback"))
async def help_callback_handler(client, callback_query: CallbackQuery):
    help_text = """
📝 **Bot Commands Overview:**

1. **/add userID** - Add user to premium (Owner only)
2. **/rem userID** - Remove user from premium (Owner only)
3. **/transfer userID** - Transfer premium to another user
4. **/login** - Log into the bot for private channel access
5. **/batch** - Bulk extraction for posts (After login)
6. **/logout** - Logout from the bot
7. **/stats** - Get bot statistics
8. **/plan** - Check premium plans
9. **/speedtest** - Test the server speed
10. **/terms** - Terms and conditions
11. **/cancel** - Cancel ongoing batch process
12. **/myplan** - Get details about your plans
13. **/session** - Generate Pyrogram V2 session
14. **/settings** - Personalize bot settings

**Powered by Team SPY**
    """
    
    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("« Back", callback_data="back_to_start")]
    ])
    
    await callback_query.message.edit_text(help_text, reply_markup=back_button)
    await callback_query.answer()


@app.on_callback_query(filters.regex("features_callback"))
async def features_callback_handler(client, callback_query: CallbackQuery):
    features_text = """
🚀 **Bot Features:**

✅ **File Extraction**
• Save posts from channels and groups where forwarding is restricted
• Easily fetch messages from public channels by sending their post links
• For private channels, use /login to access content securely

✅ **Bulk Operations**
• Download up to 100,000 files in a single batch command
• Two modes available: /bulk and /batch
• Automatic process management

✅ **Premium Features**
• Extended download limits
• Priority processing
• All functions unlocked
• No time restrictions

✅ **Security**
• Secure session management
• Safe private channel access
• Protected data handling

✅ **Additional Tools**
• Speed test functionality
• Session generation
• Custom settings
• Transfer capabilities

**Ready to get started? Use /help for commands!**
    """
    
    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("« Back", callback_data="back_to_start")]
    ])
    
    await callback_query.message.edit_text(features_text, reply_markup=back_button)
    await callback_query.answer()


@app.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_handler(client, callback_query: CallbackQuery):
    join_button = InlineKeyboardButton("𝐉𝐨𝐢𝐧 𝐌𝐚𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url="https://t.me/wabxbots/3")
    premium = InlineKeyboardButton("𝐑𝐞𝐩𝐨𝐫𝐭 𝐄𝐫𝐫𝐨𝐫𝐬", url="https://t.me/")
    help_button = InlineKeyboardButton("Help", callback_data="help_callback")
    features_button = InlineKeyboardButton("Features", callback_data="features_callback")
    keyboard = InlineKeyboardMarkup([
        [join_button],   
        [premium],
        [help_button, features_button]    
    ])
    
    start_text = (
        f"Hi {callback_query.from_user.mention} 👋 Welcome, Wanna intro...?\n\n"
        "**➭ Sᴀᴠᴇ ᴘᴏꜱᴛꜱ ғʀᴏᴍ ᴄʜᴀɴɴᴇʟꜱ ᴀɴᴅ ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ғᴏʀᴡᴀʀᴅɪɴɢ ɪꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ**\n"
        "**➭ Eᴀꜱɪʟʏ ғᴇᴛᴄʜ ᴍᴇꜱꜱᴀɢᴇꜱ ғʀᴏᴍ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ ʙʏ ꜱᴇɴᴅɪɴɢ ᴛʜᴇɪʀ ᴘᴏꜱᴛ ʟɪɴᴋꜱ**\n"
        "**➭ Fᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ, ᴜꜱᴇ /ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇꜱꜱ ᴄᴏɴᴛᴇɴᴛ ꜱᴇᴄᴜʀᴇʟʏ**\n\n"
        "**📑 Fᴏʀ ᴍᴏʀᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ ꜱᴇɴᴅ /ʜᴇʟᴘ**"
    )
    
    # Edit the current message to show the start content
    await callback_query.message.edit_text(start_text, reply_markup=keyboard)
    await callback_query.answer()


@app.on_callback_query(filters.regex("start_photo"))
async def start_photo_handler(client, callback_query: CallbackQuery):
    # This callback will be used when we need to go back to the photo version
    await callback_query.message.delete()
    
    join_button = InlineKeyboardButton("𝐉𝐨𝐢𝐧 𝐌𝐚𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url="https://t.me/wabxbots/3")
    premium = InlineKeyboardButton("𝐑𝐞𝐩𝐨𝐫𝐭 𝐄𝐫𝐫𝐨𝐫𝐬", url="https://t.me/")
    help_button = InlineKeyboardButton("Help", callback_data="help_callback")
    features_button = InlineKeyboardButton("Features", callback_data="features_callback")
    keyboard = InlineKeyboardMarkup([
        [join_button],   
        [premium],
        [help_button, features_button]    
    ])
    
    caption = (
        f"Hi {callback_query.from_user.mention} 👋 Welcome, Wanna intro...?\n\n"
        "**➭ Sᴀᴠᴇ ᴘᴏꜱᴛꜱ ғʀᴏᴍ ᴄʜᴀɴɴᴇʟꜱ ᴀɴᴅ ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ғᴏʀᴡᴀʀᴅɪɴɢ ɪꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ**\n"
        "**➭ Eᴀꜱɪʟʏ ғᴇᴛᴄʜ ᴍᴇꜱꜱᴀɢᴇꜱ ғʀᴏᴍ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ ʙʏ ꜱᴇɴᴅɪɴɢ ᴛʜᴇɪʀ ᴘᴏꜱᴛ ʟɪɴᴋꜱ**\n"
        "**➭ Fᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ, ᴜꜱᴇ /ʟᴏɢɪɴ ᴛᴏ ᴀᴄᴄᴇꜱꜱ ᴄᴏɴᴛᴇɴᴛ ꜱᴇᴄᴜʀᴇʟʏ**\n\n"
        "**📑 Fᴏʀ ᴍᴏʀᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ ꜱᴇɴᴅ /ʜᴇʟᴘ**"
    )
    
    # Send a new message with the image from config
    await callback_query.message.reply_photo(
        START_IMAGE_URL,
        caption=caption,
        reply_markup=keyboard
    )
    
    await callback_query.answer()
