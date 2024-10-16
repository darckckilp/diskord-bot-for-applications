import disnake
from disnake.ext import commands


class RecruitementModal(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg
        components = [
            disnake.ui.TextInput(label="Your nickname on the server", placeholder="Enter your nickname", custom_id="name"),
            disnake.ui.TextInput(label="Your age", placeholder="Enter your age", custom_id="age"),
            disnake.ui.TextInput(label="How familiar are you with the rules?", placeholder="Rules from 1 to 10", custom_id="rul"),
            disnake.ui.TextInput(label="Tell us about yourself", placeholder="Tell us about yourself", custom_id="zach")
        ]
        if self.arg == "moderator":
            title = "Recruitment for the position of moderator"
        else:
            title = "Recruitment for the position of support"
        super().__init__(title=title, components=components, custom_id="recruitementModal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = interaction.text_values["name"]
        age = interaction.text_values["age"]
        rul = interaction.text_values["rul"]
        zach = interaction.text_values["zach"]
        embed = disnake.Embed(color=0x2F3136, title="Application sent!")
        embed.description = f"{interaction.author.mention}, Thank you for your **request**! " \
                            f"If you are **suitable** for us, the administration will **contact** you shortly."
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        channel = interaction.guild.get_channel(...) #channel id where you need to send a message
        await channel.send(f"Application for the position {self.arg} from {interaction.author.mention}\nserver nickname: ``{name}``\nage: {age}\nknowing the rules: {rul}\nabout myself:\n{zach}")


class RecruitementSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="moderator", value="moderator", description="moderator"),
            disnake.SelectOption(label="support", value="support", description="support"),
        ]
        super().__init__(
            placeholder="Choose the role you want to go for", options=options, min_values=0, max_values=1, custom_id="recruitement"
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        if not interaction.values:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(RecruitementModal(interaction.values[0]))


class Recruitement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.slash_command()
    async def recruit(self, ctx):
        """team recruitment."""
        view = disnake.ui.View()
        view.add_item(RecruitementSelect())
        await ctx.send('Выбери роль на которую хотите пойти.\n**ATTENTION!!/n **For** repeated **or** joking requests, you will receive a mute for **two or more weeks**', view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(RecruitementSelect())
        self.bot.add_view(view,
                          message_id=1158456209645514772)


def setup(bot):
    bot.add_cog(Recruitement(bot))