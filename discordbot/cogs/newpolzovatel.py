import disnake
from disnake.ext import commands


class acceptuserModal(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg
        components = [
            disnake.ui.TextInput(label="who was accepted", custom_id="user"),
        ]
        if self.arg == "moderator":
            title = "moderator"
        else:
            title = "support"
        super().__init__(title=title, components=components, custom_id="acceptuserModal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        user = interaction.text_values["user"]
        embed = disnake.Embed(color=0x2F3136, title="The person has been accepted!")
        embed.description = f"I warned the user {interaction.author.mention}"
        await interaction.response.send_message(embed=embed, ephemeral=True)

class acceptuserSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="moderator", value="moderator", description="accept as moderator"),
            disnake.SelectOption(label="support", value="support", description="Accept on Support")
        ]
        super().__init__(
            placeholder="Select the role the user was accepted to.", options=options, min_values=0, max_values=1, custom_id="acceptuser"
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        if not interaction.values:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(acceptuserModal(interaction.values[0]))


class acceptuser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.slash_command()
    async def acceptuser(self, ctx, member: disnake.Member, role: disnake.Role):
        """Grants the user role rights and sends a message to the user that he has been accepted."""
        embed = disnake.Embed(
            title="You have been accepted",
            color=disnake.Colour.purple(),
        )

        embed.add_field(name="Your application has been approved!", value="You have been accepted!\nAnd now you can read the rules for the staff\nIf there are any problems, write to PM <your id name>", inline=False)

        await member.send(embed=embed)
        await member.add_roles(role)
        view = disnake.ui.View()
        view.add_item(acceptuserSelect())
        await ctx.send('Select the role the user was accepted to.', view=view)


    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(acceptuserSelect())
        self.bot.add_view(view,
                          message_id=1158456209645514772)


def setup(bot):
    bot.add_cog(acceptuser(bot))