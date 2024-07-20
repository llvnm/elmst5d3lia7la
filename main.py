import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# تشغيل DiscordComponents
@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}")

class BotSystem:
    def __init__(self):
        self.banned_words = ["badword1", "badword2"]
        self.tickets = []
        self.message_count = {}
        self.admin_logs = []
        self.user_levels = {}
        self.admin_requests = {}
        self.logs = []
        self.owner_role = "Owner"  # رتبة الأونر
        self.level_up_thresholds = {1: 10, 2: 100}  # حدود المستويات
        self.level_up_increment = 100  # زيادة المستوى بعد 100 رسالة
        self.channels = {}  # للحفاظ على معلومات القنوات

    # نظام الحماية
    def check_message(self, user, message):
        if any(word in message.lower() for word in self.banned_words):
            return "Message blocked due to inappropriate content."
        return "Message allowed."

    def protect_owner_actions(self, user, action):
        if isinstance(user, discord.Member) and self.owner_role in [role.name for role in user.roles]:
            return "Action not allowed for Owners."
        return "Action allowed."

    def prevent_channel_creation(self, channel_name):
        # هنا يمكن استخدام API لحذف القناة
        return f"Channel '{channel_name}' has been deleted."

    def notify_on_message(self, room, image_url):
        return f"Notification in {room}: Please check the image {image_url}."

    # نظام المستويات
    def update_user_level(self, user):
        if user not in self.message_count:
            self.message_count[user] = 0
        self.message_count[user] += 1

        # حساب المستوى
        level = 1
        for threshold, message_count in self.level_up_thresholds.items():
            if self.message_count[user] >= message_count:
                level = threshold

        if self.message_count[user] > self.level_up_thresholds.get(level, float('inf')):
            level += 1

        self.user_levels[user] = level
        return f"{user} is now at level {self.user_levels[user]}."

    # نظام التذاكر
    def create_ticket(self, user, issue):
        ticket_id = len(self.tickets) + 1
        self.tickets.append({'id': ticket_id, 'user': user, 'issue': issue})
        return f"Ticket {ticket_id} created for {user}."

    # حماية القنوات
    def backup_channel(self, channel_name, messages):
        self.channels[channel_name] = messages

    def restore_channel(self, channel_name):
        if channel_name in self.channels:
            # هنا يمكن استخدام API لإنشاء القناة وإعادة الرسائل
            return f"Channel '{channel_name}' has been restored with all messages and files."
        return f"Channel '{channel_name}' not found in backup."

    # سجل متطور
    def add_log(self, event):
        self.logs.append(event)

    def log_action(self, action_type, content):
        self.logs.append({'action_type': action_type, 'content': content})

# استخدام البوت
bot_system = BotSystem()

# الدالة لإنشاء تذكرة
async def create_ticket(interaction, ticket_type):
    user = interaction.author
    ticket_channel = await interaction.guild.create_text_channel(f"{ticket_type}-{user.name}")
    await ticket_channel.send(f"{user.mention} created a ticket for {ticket_type}.")
    await interaction.send(content=f"Ticket for {ticket_type} created!", ephemeral=True)

# أمر لإنشاء رسالة تذكرة
@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="Mlwn Service",
        description="Open a ticket with your reason.",
        color=discord.Color.blue()
    )

    buttons = [
        Button(style=ButtonStyle.blue, label="Help", custom_id="help_ticket"),
        Button(style=ButtonStyle.blue, label="Support", custom_id="support_ticket"),
        Button(style=ButtonStyle.blue, label="Inquiry", custom_id="inquiry_ticket"),
        Button(style=ButtonStyle.blue, label="Problem", custom_id="problem_ticket"),
        Button(style=ButtonStyle.blue, label="Reports", custom_id="reports_ticket")
    ]

    await ctx.send(embed=embed, components=buttons)

# التعامل مع الضغط على الأزرار
@bot.event
async def on_button_click(interaction):
    custom_id_to_type = {
        "help_ticket": "Help",
        "support_ticket": "Support",
        "inquiry_ticket": "Inquiry",
        "problem_ticket": "Problem",
        "reports_ticket": "Reports"
    }

    ticket_type = custom_id_to_type.get(interaction.custom_id)
    if ticket_type:
        await create_ticket(interaction, ticket_type)

# تشغيل البوت
bot.run('MTI2MTYwNTU4MjkzOTYyMzQ3NQ.Gt130O.ebj9cJhASuPEI8S0OJHniMhBN2TdkZ5X8fRKs0')
